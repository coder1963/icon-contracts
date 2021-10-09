import json
import os
import shutil

from google.protobuf.json_format import MessageToJson
from sqlalchemy.orm import sessionmaker

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.metrics import Metrics
from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_proto import contract_to_proto
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.utils.contract_content import (
    get_contract_name,
    upload_to_s3,
    zip_content_to_dir,
)
from icon_contracts.utils.rpc import icx_call, icx_getTransactionResult
from icon_contracts.workers.db import engine
from icon_contracts.workers.kafka import Worker

metrics = Metrics()


class TransactionsWorker(Worker):

    msg_count: int = 0
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    def process_contract_creation(self):
        pass

    def java_contract(self, content, value):
        pass

    def python_contract(self, content: str, value: TransactionRaw):
        tx_result = icx_getTransactionResult(value.hash).json()["result"]

        address = tx_result["scoreAddress"]
        timestamp = int(value.timestamp, 16)

        # Check if there is a contract in the DB with that address otherwise create it
        contract = self.session.get(Contract, address)

        if contract is None:
            # In order process
            logger.info(
                f"Creating new contract address = {address} at block = {value.block_number}"
            )
            contract = Contract(
                address=address,
                name=get_contract_name(address),
                owner_address=value.from_address,
                last_updated_block=value.block_number,
                # last_updated_timestamp=timestamp, # Out on purpose for subsequent logic
                created_block=value.block_number,
                created_timestamp=timestamp,
                status="Submitted",
            )

        # Out of order processes
        # Checking last_updated_timestamp case for when we see a contract approval
        # event before we see the contract submission
        if (
            value.block_number > contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(f"Updating contract address = {address} at block = {value.block_number}")
            self.contracts_updated_python += 1
            metrics.contracts_created_python.set(self.contracts_updated_python)

            # If we have access credentials
            if settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY:
                # Increment the revision number
                contract.revision_number = +1
                zip_name = f"{contract.address}_{contract.revision_number}.zip"
                # Unzip the contents of the dict to a directory
                contract_path = zip_content_to_dir(content, zip_name)
                # Upload to
                upload_to_s3(contract_path, zip_name)
                contract.source_code_link = (
                    f"https://{settings.CONTRACTS_S3_BUCKET}.s3.us-west-2.amazonaws.com/{zip_name}"
                )
                # Cleanup
                shutil.rmtree(os.path.dirname(contract_path))
                logger.info(f"Uploaded contract to {contract.source_code_link}")
            else:
                logger.info(f"Skip uploading tx {value.hash}")

            contract.name = get_contract_name(contract.address)
            contract.last_updated_block = value.block_number
            contract.last_updated_timestamp = timestamp

        # Condition where we have already updated the record
        if (
            value.block_number < contract.last_updated_block
            or contract.last_updated_timestamp is None
        ):
            logger.info(
                f"Updating contract creation for address = {address} at block = {value.block_number}"
            )
            contract.created_block = value.block_number
            contract.created_timestamp = timestamp

        # Method that classifies the contract based on ABI for IRC2 stuff
        contract.extract_contract_details()

        self.produce_protobuf(
            settings.PRODUCER_TOPIC_CONTRACTS,
            value.hash,  # Keyed on hash
            contract_to_proto(contract),
        )

        # Commit the contract
        self.session.add(contract)
        self.session.commit()

    def process_audit(self, value: TransactionRaw):
        data = json.loads(value.data)

        # Contract creation events
        if "contentType" in data:
            logger.info(f"Unknown event for with hash = {value.hash}")
            # No idea what is going on here.
            self.produce_json(
                topic=settings.PRODUCER_TOPIC_DLQ,
                key="unknown-event-content-type",
                value=MessageToJson(value),
            )
            self.json_producer.poll(0)
            return

        # Audit related events
        if data["method"] in ["acceptScore", "rejectScore"]:
            address = icx_getTransactionResult(data["params"]["txHash"]).json()["result"][
                "scoreAddress"
            ]

            # Make the status the address in case there is some funky situation
            # we don't know about -> proxy for dead letter queue
            status = address
            if data["method"] == "acceptScore":
                status = "Accepted"
            elif data["method"] == "rejectScore":
                status = "Rejected"

            contract = self.session.get(Contract, address)

            if contract is None:
                logger.info(
                    f"Creating contract from approval for address = {address} at block = {value.block_number}"
                )
                self.contracts_created_python += 1
                metrics.contracts_created_python.set(self.contracts_created_python)
                contract = Contract(
                    address=address,
                    name=get_contract_name(address),
                    status=status,
                    owner_address=value.from_address,
                    last_updated_block=value.block_number,
                    # last_updated_timestamp=timestamp, # Out on purpose for subsequent logic
                    created_block=value.block_number,
                    created_timestamp=int(value.timestamp, 16),
                )
            else:
                logger.info(
                    f"Updating contract status from approval for address = {address} at block = {value.block_number}"
                )
                self.contracts_updated_python += 1
                metrics.contracts_created_python.set(self.contracts_updated_python)

                contract.status = status

            self.produce_protobuf(
                settings.PRODUCER_TOPIC_CONTRACTS,
                value.hash,  # Keyed on hash
                contract_to_proto(contract),
            )

            self.session.add(contract)
            self.session.commit()

    def process(self, msg):
        value = msg.value()

        if self.msg_count % 10000 == 0:
            logger.info(
                f"msg count {self.msg_count} and block {value.block_number} "
                f"for consumer group {self.consumer_group}"
            )
            metrics.block_height.set(value.block_number)
        self.msg_count += 1

        # Pass on any invalid Tx in this service
        if value.receipt_status != 1:
            return

        # Messages are keyed by to_address
        if msg.key() == settings.one_address:
            self.process_audit(value)

        if msg.key() == settings._governance_address and value.receipt_status == 1:

            data = json.loads(value.data)

            if "contentType" in data:
                if data["contentType"] == "application/zip":
                    self.python_contract(data["content"], value)

                if data["contentType"] == "application/java":
                    self.java_contract(data["content"], value)

            return

        # if method in 'addAuditor':
        #     print()
        #
        # if method in 'removeAuditor':
        #     print()


def transactions_worker_head():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    kafka = TransactionsWorker(
        session=session,
        topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
        consumer_group=settings.CONSUMER_GROUP_HEAD,
        auto_offset_reset="latest",
    )

    kafka.start()


def transactions_worker_tail():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    kafka = TransactionsWorker(
        session=session,
        topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
        consumer_group=settings.CONSUMER_GROUP_TAIL,
        auto_offset_reset="earliest",
    )

    kafka.start()


if __name__ == "__main__":
    # transactions_worker_head()
    transactions_worker_tail()

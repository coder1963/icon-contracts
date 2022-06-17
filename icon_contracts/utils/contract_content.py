import json
import os
import tempfile
import zipfile
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Any

import boto3
import requests
from botocore.exceptions import ClientError

from icon_contracts.config import settings
from icon_contracts.log import logger
from icon_contracts.models.verification_contract import VerificationInput
from icon_contracts.utils.rpc import icx_call
from icon_contracts.utils.shell import run_command


def zip_content_to_dir(content: str, zip_name: str) -> str:
    if content.startswith("0x"):
        content = content[2:]

    dirpath = tempfile.mkdtemp()
    contract_path = os.path.join(dirpath, zip_name)
    with open(contract_path + ".txt", "w") as f:
        f.write(content)

    command = f"xxd -r -p {contract_path}.txt > {contract_path}.zip"
    run_command(command)

    return contract_path + ".zip"


def github_release_to_dir(output_name: str, params: VerificationInput):
    gh_base_ref = f"https://github.com/{params.github_org}/{params.github_repo}"
    gh_release_ref = f"{gh_base_ref}/releases/tag/{params.github_release}"

    # Check and see if there is a release in the location
    # Done to prevent users from using a branch which is mutable
    r = requests.get(gh_release_ref)
    if r.status_code != 200:
        raise Exception(f"Failed to clone {gh_release_ref} - non 200 code")

    dirpath = tempfile.mkdtemp()
    os.chdir(dirpath)

    p = Popen(
        ["git", "clone", gh_base_ref, "--branch", params.github_release, output_name],
        stdout=PIPE,
        stderr=PIPE,
    )
    _, error = p.communicate()
    if p.returncode != 0:
        raise Exception(f"Failed to clone {gh_release_ref} with error {error}")

    if params.github_directory == "":
        return dirpath, os.path.join(dirpath, output_name)
    else:
        output_path = os.path.join(dirpath, output_name, params.github_directory)
        if os.path.isdir(output_path):
            return dirpath, output_path
        else:
            raise Exception(f"Cloud not clone with dir {output_path}")


def unzip_get_sha(zip_path: str):
    """Unzip the contents of zip_path and return sha of source """
    pass


def get_s3_client():
    if settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY:
        return boto3.client(
            "s3",
            aws_access_key_id=settings.CONTRACTS_S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CONTRACTS_S3_AWS_SECRET_ACCESS_KEY,
        )
    else:
        return None


def upload_to_s3(s3_client: Any, filename: str, key: str, prefix: str = "contract-sources"):
    # Can't share client across threads
    # https://github.com/boto/botocore/issues/1246
    if s3_client is None:
        logger.info(f"Skipping S3 upload for filename {filename}.")
        return
    s3_client.upload_file(filename, settings.CONTRACTS_S3_BUCKET, f"{prefix}/" + key)


def get_contract_name(address):
    name_response = icx_call(address, {"method": "name"})
    if name_response is not None and name_response.status_code == 200:
        return icx_call(address, {"method": "name"}).json()["result"]
    else:
        return ""


# TODO: This is viable if we want to keep track of the contracts
#  stored in s3 but we really don't care that much. We track it
#  in the db and overwrite so...
# def determine_s3_contract_key(address: str):
#     """Make the """
#     s3 = get_s3_client()
#
#     revision_counter = 1
#     while revision_counter:
#         if revision_counter > 50:
#             logger.info(f"Maximum number of revisions for {address}.")
#
#         try:
#             response = s3.get_object(Bucket=settings.CONTRACTS_S3_BUCKET,
#                                      Key=address + f'_{revision_counter}.zip')
#             return json.loads(response["Body"].read())
#         except ClientError as ex:
#             if ex.response['Error']['Code'] == 'NoSuchKey':
#                 revision_counter += 1
#                 continue
#             else:
#                 raise


# def extract_content_to_path(src, dest):
#     with zipfile.ZipFile(src, "r") as zip_ref:
#         zip_ref.extractall(dest)
#
#     files = os.listdir(dest)
#     f = None
#     for f in files:
#         if os.path.isdir(os.path.join(dest, f)):
#             break
#
#     if f is None:
#         raise ValueError("Could not find zip output directory. Buh?")
#
#     return os.path.join(dest, f)
#
#
# def import_score(score_dir):
#     pass
#
#
# def find_and_load_package_json(contract_path) -> Union[dict, NotADirectoryError]:
#     # Find the path to the first package.json
#     for path in Path(contract_path).rglob("package.json"):
#         # Extract the package_json
#         with open(path) as file:
#             return json.load(file)
#     return NotADirectoryError(f"Could not find package.json in {contract_path}")


# if __name__ == "__main__":
#     x = find_and_load_package_json("/tmp/tmpci_lmje5/")
#     print()

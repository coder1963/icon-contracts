"""add owner address

Revision ID: f261d56b3b41
Revises: e0bb0641752e
Create Date: 2021-10-05 01:58:38.013093

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "f261d56b3b41"
down_revision = "e0bb0641752e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contract", sa.Column("owner_address", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    op.create_index(op.f("ix_contract_owner_address"), "contract", ["owner_address"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_contract_owner_address"), table_name="contract")
    op.drop_column("contract", "owner_address")
    # ### end Alembic commands ###

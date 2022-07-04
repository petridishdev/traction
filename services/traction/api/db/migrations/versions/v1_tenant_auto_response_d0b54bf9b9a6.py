"""v1-tenant-auto-response

Revision ID: d0b54bf9b9a6
Revises: 78d0d1c2b87a
Create Date: 2022-06-16 14:06:59.152577

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d0b54bf9b9a6"
down_revision = "78d0d1c2b87a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tenant_auto_response_log",
        sa.Column("tenant_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("contact_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("message", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.contact_id"],
        ),
        sa.PrimaryKeyConstraint("tenant_id"),
    )
    op.create_index(
        op.f("ix_tenant_auto_response_log_tenant_id"),
        "tenant_auto_response_log",
        ["tenant_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_tenant_auto_response_log_tenant_id"),
        table_name="tenant_auto_response_log",
    )
    op.drop_table("tenant_auto_response_log")
    # ### end Alembic commands ###
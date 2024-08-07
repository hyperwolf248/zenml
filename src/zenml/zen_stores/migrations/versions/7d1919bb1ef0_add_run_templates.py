"""Add run templates [7d1919bb1ef0].

Revision ID: 7d1919bb1ef0
Revises: b59aa68fdb1f
Create Date: 2024-07-22 11:20:00.544451

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "7d1919bb1ef0"
down_revision = "b59aa68fdb1f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "run_template",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "description",
            sa.String(length=16777215).with_variant(mysql.MEDIUMTEXT, "mysql"),
            nullable=True,
        ),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column(
            "workspace_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column(
            "source_deployment_id", sqlmodel.sql.sqltypes.GUID(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["source_deployment_id"],
            ["pipeline_deployment.id"],
            name="fk_run_template_source_deployment_id_pipeline_deployment",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="fk_run_template_user_id_user",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspace.id"],
            name="fk_run_template_workspace_id_workspace",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "name", "workspace_id", name="unique_template_name_in_workspace"
        ),
    )
    with op.batch_alter_table("pipeline_build", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "stack_checksum",
                sqlmodel.sql.sqltypes.AutoString(),
                nullable=True,
            )
        )
        batch_op.drop_column("template_deployment_id")

    with op.batch_alter_table("pipeline_deployment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "template_id", sqlmodel.sql.sqltypes.GUID(), nullable=True
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pipeline_deployment", schema=None) as batch_op:
        batch_op.drop_column("template_id")

    with op.batch_alter_table("pipeline_build", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "template_deployment_id", sa.CHAR(length=32), nullable=True
            )
        )
        batch_op.drop_column("stack_checksum")

    op.drop_table("run_template")
    # ### end Alembic commands ###

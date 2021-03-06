"""init

Revision ID: 0d18dd8b3ec9
Revises: 
Create Date: 2021-12-10 03:01:42.710026

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0d18dd8b3ec9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "access_level",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "name",
            sa.Enum("UNREGISTERED", "BLOCKED", "USER", "ADMINISTRATOR", name="levels"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "currency",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "department",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inform_level",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cost",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("department_id", sa.INTEGER(), nullable=True),
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["department.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_access_levels",
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("access_level_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["access_level_id"],
            ["access_level.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id", "access_level_id"),
    )
    op.create_table(
        "confirmation_path",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("cost_id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cost_id"],
            ["cost.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cost_id", "user_id", name="_user_cost"),
    )
    op.create_table(
        "confirmation_path_chief",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("confirmation_path_id", sa.INTEGER(), nullable=False),
        sa.Column("chief_id", sa.BIGINT(), nullable=False),
        sa.Column("inform_level_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chief_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["confirmation_path_id"],
            ["confirmation_path.id"],
        ),
        sa.ForeignKeyConstraint(
            ["inform_level_id"],
            ["inform_level.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("confirmation_path_id", sa.INTEGER(), nullable=False),
        sa.Column("amount", sa.REAL(), nullable=False),
        sa.Column("vat", sa.BOOLEAN(), nullable=False),
        sa.Column("currency", sa.INTEGER(), nullable=False),
        sa.Column("cost_id", sa.INTEGER(), nullable=False),
        sa.Column("comment", sa.TEXT(), nullable=False),
        sa.Column("chief_confirm", sa.BOOLEAN(), nullable=True),
        sa.Column("date", sa.TIMESTAMP(), nullable=False),
        sa.Column("date_confirm", sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["confirmation_path_id"],
            ["confirmation_path.id"],
        ),
        sa.ForeignKeyConstraint(
            ["cost_id"],
            ["cost.id"],
        ),
        sa.ForeignKeyConstraint(
            ["currency"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("order")
    op.drop_table("confirmation_path_chief")
    op.drop_table("confirmation_path")
    op.drop_table("user_access_levels")
    op.drop_table("cost")
    op.drop_table("user")
    op.drop_table("inform_level")
    op.drop_table("department")
    op.drop_table("currency")
    op.drop_table("access_level")
    # ### end Alembic commands ###

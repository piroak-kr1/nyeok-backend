"""Place table: Add coordinate column

Revision ID: 7ea8425668d0
Revises: 367de4fb88e6
Create Date: 2024-08-23 20:51:45.216316

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision: str = "7ea8425668d0"
down_revision: Union[str, None] = "367de4fb88e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "place",
        sa.Column(
            "coordinate",
            Geometry(
                geometry_type="POINT",
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
    )
    # NOTE: add_column already creates an index
    # op.create_index(
    #     "idx_place_coordinate",
    #     "place",
    #     ["coordinate"],
    #     unique=False,
    #     postgresql_using="gist",
    # )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_place_coordinate", table_name="place", postgresql_using="gist")
    op.drop_column("place", "coordinate")
    # ### end Alembic commands ###

"""update_11

Revision ID: 1afd43a013dc
Revises: 
Create Date: 2024-03-21 16:10:50.874444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1afd43a013dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('referal_program_cod_key', 'referal_program', type_='unique')
    op.drop_column('referal_program', 'cod')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('referal_program', sa.Column('cod', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('referal_program_cod_key', 'referal_program', ['cod'])
    # ### end Alembic commands ###
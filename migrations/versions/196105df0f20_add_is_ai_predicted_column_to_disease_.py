"""Add is_ai_predicted column to Disease model

Revision ID: 196105df0f20
Revises: 4a1a3a9f4cb5
Create Date: 2025-05-17 14:29:50.372625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '196105df0f20'
down_revision = '4a1a3a9f4cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disease', sa.Column('is_ai_predicted', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_message_is_read'), 'message', ['is_read'], unique=False)
    op.create_index(op.f('ix_prediction_is_reviewed'), 'prediction', ['is_reviewed'], unique=False)
    op.create_index(op.f('ix_prediction_reviewed_by'), 'prediction', ['reviewed_by'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prediction_reviewed_by'), table_name='prediction')
    op.drop_index(op.f('ix_prediction_is_reviewed'), table_name='prediction')
    op.drop_index(op.f('ix_message_is_read'), table_name='message')
    op.drop_column('disease', 'is_ai_predicted')
    # ### end Alembic commands ###

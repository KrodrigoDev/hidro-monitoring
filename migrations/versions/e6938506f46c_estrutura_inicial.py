"""estrutura inicial

Revision ID: e6938506f46c
Revises: 
Create Date: 2025-10-27 09:50:16.203879
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Identificadores da revisão
revision: str = 'e6938506f46c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Criação inicial das tabelas."""

    # === Tabela empresa ===
    op.create_table(
        'empresa',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now())
    )

    # === Tabela usuario ===
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(120), nullable=False),
        sa.Column('sobrenome', sa.String(120), nullable=True),
        sa.Column('cpf', sa.String(14), unique=True, nullable=False),
        sa.Column('senha', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
        sa.Column('id_empresa', sa.Integer(), sa.ForeignKey('empresa.id', ondelete='CASCADE'))
    )

    # === Tabela local_equipamento ===
    op.create_table(
        'local_equipamento',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('municipio', sa.String(120), nullable=True),
        sa.Column('bairro', sa.String(120), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True)
    )

    # === Tabela equipamento ===
    op.create_table(
        'equipamento',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ult_manutencao', sa.Date(), nullable=True),
        sa.Column('nome', sa.String(100), nullable=True),
        sa.Column('ult_limpeza', sa.Date(), nullable=True),
        sa.Column('tipo', sa.String(120), nullable=True),
        sa.Column('situacao', sa.String(120), nullable=True),
        sa.Column('voltagem', sa.String(50), nullable=True),
        sa.Column('vazao', sa.String(50), nullable=True),
        sa.Column('profundidade', sa.String(50), nullable=True),
        sa.Column('id_local_equipamento', sa.Integer(), sa.ForeignKey('local_equipamento.id', ondelete='SET NULL')),
        sa.Column('id_empresa', sa.Integer(), sa.ForeignKey('empresa.id', ondelete='SET NULL'))
    )

    op.create_table('log',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('acao', sa.String(), nullable=True),  # criar, alterar, editar e excluir
                    sa.Column('id_usuario', sa.Integer(), sa.ForeignKey('usuario.id')),
                    sa.Column('id_equipamento', sa.Integer(), sa.ForeignKey('equipamento.id')),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now())
                    )


def downgrade() -> None:
    """Reverte a estrutura criada no upgrade."""
    op.drop_table('log')
    op.drop_table('equipamento')
    op.drop_table('local_equipamento')
    op.drop_table('usuario')
    op.drop_table('empresa')


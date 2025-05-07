from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float,
    DateTime, Boolean, func, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    idade = Column(Integer)
    ativo = Column(Boolean, default=True)
    pedidos = relationship('Pedido', back_populates='usuario')

    def __str__(self):
        return f"{self.id}, {self.nome}, {self.email}, {self.idade}, {self.ativo}"

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))
    estoque = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.now)

    def __str__(self):
        criado_em_str = self.criado_em.strftime("%Y-%m-%d %H:%M:%S") if self.criado_em else "None"
        return f"{self.id}, {self.nome}, {self.preco}, {self.categoria}, {self.estoque}, {criado_em_str}"

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    status = Column(String(20), default='pendente')
    data_pedido = Column(DateTime, default=datetime.now)
    
    usuario = relationship('Usuario', back_populates='pedidos')
    produto = relationship('Produto')
    
    __table_args__ = (
        UniqueConstraint('usuario_id', 'produto_id', name='uq_usuario_produto'),
    )

    def __str__(self):
        data_pedido_str = self.data_pedido.strftime("%Y-%m-%d %H:%M:%S") if self.data_pedido else "None"
        return f"{self.id}, {self.usuario_id}, {self.produto_id}, {self.quantidade}, {self.status}, {data_pedido_str}"

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(String(300))
    
    usuario = relationship('Usuario')

    def __str__(self):
        return f"{self.id}, {self.usuario_id}, {self.nota}, {self.comentario}"
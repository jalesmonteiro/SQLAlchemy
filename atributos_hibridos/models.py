from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float,
    DateTime, Boolean, func, UniqueConstraint,
    case, select, func, text
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
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
    avaliacoes = relationship('Avaliacao', back_populates='usuario')

    
    def __str__(self):
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', idade={self.idade}, ativo={self.ativo})"
    
    @hybrid_property
    def status_idade(self):
        return "adulto" if self.idade >= 18 else "jovem"

    @status_idade.expression
    def status_idade(cls):
        return case(
            (cls.idade >= 18, "adulto"),
            else_="jovem"
        )

    @hybrid_property
    def total_pedidos(self):
        return len(self.pedidos)  # Funciona em objetos carregados

    @total_pedidos.expression
    def total_pedidos(cls):
        return (
            select(func.count(Pedido.id))
            .where(Pedido.usuario_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )
        
    @hybrid_property
    def dominio_email(self):
        return self.email.split("@")[-1] if "@" in self.email else None

    @dominio_email.expression
    def dominio_email(cls):
        return func.substring_index(cls.email, "@", -1)
    
    @hybrid_property
    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0.0
        return sum(av.nota for av in self.avaliacoes) / len(self.avaliacoes)

    @media_avaliacoes.expression
    def media_avaliacoes(cls):
        return (
            select(func.avg(Avaliacao.nota))
            .where(Avaliacao.usuario_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )
    
    @hybrid_property
    def tem_pedido_recente(self):
        if not self.pedidos:
            return False
        ultimo_pedido = max(p.data_pedido for p in self.pedidos)
        return (datetime.now() - ultimo_pedido).days <= 7

    @tem_pedido_recente.expression
    def tem_pedido_recente(cls):
        return (
            select(func.max(Pedido.data_pedido))
            .where(Pedido.usuario_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
            >= text("CURRENT_DATE - INTERVAL '7 DAYS'")
        )

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))
    estoque = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.now)
    
    def __str__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', preco={self.preco}, categoria='{self.categoria}', estoque={self.estoque}, criado_em={self.criado_em})"

    @hybrid_property
    def preco_com_imposto(self):
        return round(self.preco * 1.10, 2)  # 10% de imposto

    @preco_com_imposto.expression
    def preco_com_imposto(cls):
        return cls.preco * 1.10
    
    @hybrid_property
    def status_estoque(self):
        if self.estoque == 0:
            return "esgotado"
        elif self.estoque <= 10:
            return "baixo"
        else:
            return "suficiente"

    @status_estoque.expression
    def status_estoque(cls):
        return case(
            (cls.estoque == 0, "esgotado"),
            (cls.estoque <= 10, "baixo"),
            else_="suficiente"
        )

    @hybrid_property
    def idade_dias(self):
        return (datetime.now() - self.criado_em).days

    @idade_dias.expression
    def idade_dias(cls):
        return func.extract('day', func.age(func.current_date(), cls.criado_em))

    @hybrid_property
    def categoria_abreviada(self):
        return self.categoria[:3].upper() if self.categoria else None

    @categoria_abreviada.expression
    def categoria_abreviada(cls):
        return func.upper(func.left(cls.categoria, 3))

    @hybrid_property
    def em_promocao(self):
        return (datetime.now() - self.criado_em).days > 30

    @em_promocao.expression
    def em_promocao(cls):
        return cls.criado_em < text("CURRENT_DATE - INTERVAL '30 DAYS'")
    
    @hybrid_property
    def valor_total_estoque(self):
        return self.preco * self.estoque

    @valor_total_estoque.expression
    def valor_total_estoque(cls):
        return cls.preco * cls.estoque

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
        return f"Pedido(id={self.id}, usuario_id={self.usuario_id}, produto_id={self.produto_id}, quantidade={self.quantidade}, status='{self.status}', data_pedido={self.data_pedido})"

    @hybrid_property
    def total(self):
        return self.quantidade * self.produto.preco  # Requer carregamento do relacionamento

    @total.expression
    def total(cls):
        return (
            select(cls.quantidade * Produto.preco)
            .where(Produto.id == cls.produto_id)
            .correlate(cls)
            .scalar_subquery()
        )

    @hybrid_property
    def pedido_recente(self):
        return (datetime.now() - self.data_pedido).days <= 7

    @pedido_recente.expression
    def pedido_recente(cls):
        return cls.data_pedido >= text("CURRENT_DATE - INTERVAL '7 DAYS'")

    @hybrid_property
    def status_prioritario(self):
        return "prioritário" if self.quantidade > 10 else "normal"

    @status_prioritario.expression
    def status_prioritario(cls):
        return case(
            (cls.quantidade > 10, "prioritário"),
            else_="normal"
        )

    @hybrid_property
    def mes_ano_pedido(self):
        return self.data_pedido.strftime("%Y-%m")

    @mes_ano_pedido.expression
    def mes_ano_pedido(cls):
        return func.to_char(cls.data_pedido, 'YYYY-MM')  # PostgreSQL
    
    @hybrid_property
    def dias_desde_pedido(self):
        return (datetime.now() - self.data_pedido).days

    @dias_desde_pedido.expression
    def dias_desde_pedido(cls):
        return func.extract('day', func.age(func.current_date(), cls.data_pedido))

    @hybrid_property
    def estoque_suficiente(self):
        return self.produto.estoque >= self.quantidade  # Requer carregamento do produto

    @estoque_suficiente.expression
    def estoque_suficiente(cls):
        return (
            select(Produto.estoque >= cls.quantidade)
            .where(Produto.id == cls.produto_id)
            .correlate(cls)
            .scalar_subquery()
        )

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(String(300))
    usuario = relationship('Usuario', back_populates='avaliacoes')

    def __str__(self):
        return f"Avaliacao(id={self.id}, usuario_id={self.usuario_id}, nota={self.nota}, comentario='{self.comentario}')"

    @hybrid_property
    def classificacao(self):
        if self.nota >= 9:
            return "excelente"
        elif self.nota >= 7:
            return "bom"
        elif self.nota >= 5:
            return "regular"
        else:
            return "ruim"

    @classificacao.expression
    def classificacao(cls):
        return case(
            (cls.nota >= 9, "excelente"),
            (cls.nota >= 7, "bom"),
            (cls.nota >= 5, "regular"),
            else_="ruim"
        )
        
    @hybrid_property
    def comentario_longo(self):
        return len(self.comentario or '') > 50

    @comentario_longo.expression
    def comentario_longo(cls):
        return func.length(cls.comentario) > 50
    
    @hybrid_property
    def media_usuario(self):
        if not self.usuario.avaliacoes:
            return 0.0
        return sum(av.nota for av in self.usuario.avaliacoes) / len(self.usuario.avaliacoes)

    @media_usuario.expression
    def media_usuario(cls):
        return (
            select(func.avg(Avaliacao.nota))
            .where(Avaliacao.usuario_id == cls.usuario_id)
            .correlate(cls)
            .scalar_subquery()
        )
        
    @hybrid_property
    def nota_estrelas(self):
        return "⭐" * self.nota

    @nota_estrelas.expression
    def nota_estrelas(cls):
        return func.repeat('⭐', cls.nota)
    
    @hybrid_property
    def valida(self):
        return self.nota > 3 and bool(self.comentario)

    @valida.expression
    def valida(cls):
        return (cls.nota > 3) & (cls.comentario.isnot(None))
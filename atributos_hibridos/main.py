from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import datetime
from models import Base, Usuario, Produto, Pedido, Avaliacao

engine = create_engine('sqlite:///../exercicios.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# ---------------
# --- Usuario ---
# ---------------

# Para instâncias:
usuario = Usuario(idade=25)
print(usuario.status_idade)  # Saída: "adulto"

# Em consultas:
query = session.query(Usuario).filter(Usuario.status_idade == "adulto")
# SQL gerado: CASE WHEN usuarios.idade >= 18 THEN 'adulto' ELSE 'jovem' END

# Para instâncias (requer carregamento explícito de pedidos):
usuario = session.get(Usuario, 1, options=[joinedload(Usuario.pedidos)])
print(usuario.total_pedidos)  # Saída: 3

# Em consultas:
query = session.query(Usuario.nome, Usuario.total_pedidos).order_by(Usuario.total_pedidos.desc())
# SQL gerado: SELECT usuarios.nome, (SELECT count(pedidos.id) FROM pedidos WHERE pedidos.usuario_id = usuarios.id) AS total_pedidos ...

# Para instâncias:
usuario = session.get(Usuario, 1, options=[joinedload(Usuario.avaliacoes)])
print(usuario.media_avaliacoes)  # Saída: 4.5

# Em consultas:
query = session.query(Usuario).filter(Usuario.media_avaliacoes >= 4.0)
# SQL gerado: SELECT * FROM usuarios WHERE (SELECT avg(avaliacoes.nota) FROM avaliacoes WHERE avaliacoes.usuario_id = usuarios.id) >= 4.0

# Para instâncias:
usuario = session.get(Usuario, 1, options=[joinedload(Usuario.pedidos)])
print(usuario.tem_pedido_recente)  # Saída: True/False

# Em consultas:
query = session.query(Usuario).filter(Usuario.tem_pedido_recente.is_(True))
# SQL gerado (PostgreSQL): SELECT * FROM usuarios WHERE (SELECT max(pedidos.data_pedido) FROM pedidos WHERE pedidos.usuario_id = usuarios.id) >= CURRENT_DATE - INTERVAL '7 DAYS'

# ---------------
# --- Produto ---
# ---------------

# Instância:
produto = Produto(preco=100.0)
print(produto.preco_com_imposto)  # 110.0

# Consulta:
query = session.query(Produto).filter(Produto.preco_com_imposto > 200.0)
# SQL: SELECT * FROM produtos WHERE produtos.preco * 1.1 > 200.0

# Instância:
produto = Produto(estoque=5)
print(produto.status_estoque)  # "baixo"

# Consulta:
query = session.query(Produto).filter(Produto.status_estoque == "esgotado")
# SQL: CASE WHEN produtos.estoque = 0 THEN 'esgotado' ... END = 'esgotado'

# Instância:
produto = Produto(criado_em=datetime(2025,1,1))
print(produto.idade_dias)  # 134 (depende da data atual)

# Consulta (PostgreSQL):
query = session.query(Produto).filter(Produto.idade_dias < 30)
# SQL: EXTRACT(day FROM AGE(CURRENT_DATE, produtos.criado_em)) < 30

# Instância:
produto = Produto(categoria="eletrônicos")
print(produto.categoria_abreviada)  # "ELE"

# Consulta (MySQL/PostgreSQL):
query = session.query(Produto).filter(Produto.categoria_abreviada == "ELE")
# SQL: UPPER(LEFT(produtos.categoria, 3)) = 'ELE'

# Instância:
produto = Produto(criado_em=datetime(2025,1,1))
print(produto.em_promocao)  # True (se a data atual for após 31/01/2025)

# Consulta (PostgreSQL):
query = session.query(Produto).filter(Produto.em_promocao.is_(True))
# SQL: produtos.criado_em < (CURRENT_DATE - INTERVAL '30 DAYS')

# Instância:
produto = Produto(preco=50.0, estoque=100)
print(produto.valor_total_estoque)  # 5000.0

# Consulta:
query = session.query(Produto).filter(Produto.valor_total_estoque > 10000)
# SQL: produtos.preco * produtos.estoque > 10000

# --------------
# --- Pedido ---
# --------------

# Instância (carregar produto):
pedido = session.get(Pedido, 1, options=[joinedload(Pedido.produto)])
print(pedido.total)  # 2 * 50.0 = 100.0

# Consulta:
query = session.query(Pedido).filter(Pedido.total > 500)
# SQL: SELECT * FROM pedidos WHERE (SELECT pedidos.quantidade * produtos.preco 
#       FROM produtos WHERE produtos.id = pedidos.produto_id) > 500

# Instância:
pedido = Pedido(data_pedido=datetime(2025,5,10))
print(pedido.pedido_recente)  # True (15/05/2025 - 10/05/2025 = 5 dias)

# Consulta (PostgreSQL):
query = session.query(Pedido).filter(Pedido.pedido_recente.is_(True))
# SQL: pedidos.data_pedido >= (CURRENT_DATE - INTERVAL '7 DAYS')

# Instância:
pedido = Pedido(quantidade=15)
print(pedido.status_prioritario)  # "prioritário"

# Consulta:
query = session.query(Pedido).filter(Pedido.status_prioritario == "prioritário")
# SQL: CASE WHEN pedidos.quantidade > 10 THEN 'prioritário' ELSE 'normal' END = 'prioritário'

# Instância:
pedido = Pedido(data_pedido=datetime(2025,5,10))
print(pedido.mes_ano_pedido)  # "2025-05"

# Consulta:
query = session.query(Pedido).filter(Pedido.mes_ano_pedido == "2025-05")
# SQL (PostgreSQL): to_char(pedidos.data_pedido, 'YYYY-MM') = '2025-05'

# Instância:
pedido = Pedido(data_pedido=datetime(2025,5,1))
print(pedido.dias_desde_pedido)  # 14 (em 15/05/2025)

# Consulta (PostgreSQL):
query = session.query(Pedido).filter(Pedido.dias_desde_pedido > 30)
# SQL: EXTRACT(day FROM AGE(CURRENT_DATE, pedidos.data_pedido)) > 30

# Instância (carregar produto):
pedido = session.get(Pedido, 1, options=[joinedload(Pedido.produto)])
print(pedido.estoque_suficiente)  # True se produto.estoque >= quantidade

# Consulta:
query = session.query(Pedido).filter(Pedido.estoque_suficiente.is_(False))
# SQL: SELECT * FROM pedidos WHERE (SELECT produtos.estoque >= pedidos.quantidade 
#       FROM produtos WHERE produtos.id = pedidos.produto_id) = FALSE


# -----------------
# --- Avaliação ---
# -----------------

# Instância:
avaliacao = Avaliacao(nota=8)
print(avaliacao.classificacao)  # "bom"

# Consulta:
query = session.query(Avaliacao).filter(Avaliacao.classificacao == "excelente")
# SQL: CASE WHEN avaliacoes.nota >= 9 THEN 'excelente' ... END = 'excelente'

# Instância:
avaliacao = Avaliacao(comentario="Ótimo produto, superou todas as expectativas...")
print(avaliacao.comentario_longo)  # True

# Consulta:
query = session.query(Avaliacao).filter(Avaliacao.comentario_longo.is_(True))
# SQL: length(avaliacoes.comentario) > 50

# Instância (carregar relacionamento):
avaliacao = session.get(Avaliacao, 1, options=[joinedload(Avaliacao.usuario).joinedload(Usuario.avaliacoes)])
print(avaliacao.media_usuario)  # 4.2

# Consulta:
query = session.query(Avaliacao).filter(Avaliacao.media_usuario >= 4.0)
# SQL: SELECT * FROM avaliacoes WHERE 
# (SELECT avg(avaliacoes.nota) FROM avaliacoes WHERE avaliacoes.usuario_id = avaliacoes.usuario_id) >= 4.0

# Instância:
avaliacao = Avaliacao(nota=5)
print(avaliacao.nota_estrelas)  # "⭐⭐⭐⭐⭐"

# Consulta (PostgreSQL):
query = session.query(Avaliacao).filter(Avaliacao.nota_estrelas == "⭐⭐⭐⭐⭐")
# SQL: repeat('⭐', avaliacoes.nota) = '⭐⭐⭐⭐⭐'

# Instância:
avaliacao = Avaliacao(nota=4, comentario="Bom")
print(avaliacao.valida)  # True

# Consulta:
query = session.query(Avaliacao).filter(Avaliacao.valida.is_(True))
# SQL: avaliacoes.nota > 3 AND avaliacoes.comentario IS NOT NULL
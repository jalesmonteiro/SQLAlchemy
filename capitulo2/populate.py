from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Usuario, Produto, Pedido, Avaliacao

engine = create_engine('sqlite:///exercicios.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# População de Usuários
usuarios = [
    Usuario(nome='Carlos', email='carlos@exemplo.com', idade=25, ativo=True),
    Usuario(nome='Maria', email='maria@exemplo.com', idade=30, ativo=True),
    Usuario(nome='João', email='joao@exemplo.com', idade=35, ativo=False),
    Usuario(nome='Ana', email='ana@exemplo.com', idade=28, ativo=True),
    Usuario(nome='Pedro', email='pedro@exemplo.com', idade=42, ativo=True),
    Usuario(nome='Julia', email='julia@exemplo.com', idade=19, ativo=False),
    Usuario(nome='Lucas', email='lucas@exemplo.com', idade=31, ativo=True),
    Usuario(nome='Fernanda', email='fernanda@exemplo.com', idade=27, ativo=True)
]
session.add_all(usuarios)

# População de Produtos
produtos = [
    Produto(nome='Livro Python', preco=80.0, categoria='livros', estoque=15),
    Produto(nome='Monitor 24"', preco=700.0, categoria='eletrônicos', estoque=5),
    Produto(nome='Cadeira Gamer', preco=1200.0, categoria='móveis', estoque=2),
    Produto(nome='Smartphone', preco=1500.0, categoria='eletrônicos', estoque=10),
    Produto(nome='Mesa Escritório', preco=450.0, categoria='móveis', estoque=0),
    Produto(nome='Caneta Esferográfica', preco=2.5, categoria='papelaria', estoque=100),
    Produto(nome='Notebook', preco=3500.0, categoria='eletrônicos', estoque=3),
    Produto(nome='Livro SQL', preco=95.0, categoria='livros', estoque=8)
]
session.add_all(produtos)

# População de Pedidos
pedidos = [
    # Pedidos para testes de filtros temporais
    Pedido(usuario_id=1, produto_id=1, quantidade=2, status='entregue', data_pedido=datetime(2024, 12, 15)),
    Pedido(usuario_id=2, produto_id=2, quantidade=1, status='pendente', data_pedido=datetime(2025, 1, 10)),
    Pedido(usuario_id=3, produto_id=3, quantidade=1, status='cancelado', data_pedido=datetime(2025, 2, 20)),
    Pedido(usuario_id=4, produto_id=4, quantidade=3, status='entregue', data_pedido=datetime(2025, 3, 5)),
    Pedido(usuario_id=5, produto_id=5, quantidade=1, status='pendente', data_pedido=datetime(2025, 4, 1)),
    
    # Pedidos adicionais para group_by/having
    Pedido(usuario_id=1, produto_id=6, quantidade=10, status='entregue', data_pedido=datetime(2025, 3, 10)),
    Pedido(usuario_id=1, produto_id=7, quantidade=2, status='entregue', data_pedido=datetime(2025, 3, 12)),
    Pedido(usuario_id=2, produto_id=8, quantidade=5, status='entregue', data_pedido=datetime(2025, 3, 15)),
    Pedido(usuario_id=2, produto_id=1, quantidade=3, status='entregue', data_pedido=datetime(2025, 3, 18)),
    Pedido(usuario_id=3, produto_id=2, quantidade=1, status='cancelado', data_pedido=datetime(2025, 3, 20))
]
session.add_all(pedidos)

# População de Avaliações
avaliacoes = [
    Avaliacao(usuario_id=1, nota=5, comentario='Ótimo produto'),
    Avaliacao(usuario_id=2, nota=4, comentario='Boa qualidade'),
    Avaliacao(usuario_id=3, nota=3, comentario='Regular'),
    Avaliacao(usuario_id=4, nota=2, comentario='Não recomendo'),
    Avaliacao(usuario_id=5, nota=5, comentario='Excelente'),
    Avaliacao(usuario_id=6, nota=1, comentario='Péssimo atendimento'),
    Avaliacao(usuario_id=7, nota=4, comentario='Atendimento rápido'),
    Avaliacao(usuario_id=8, nota=5, comentario='Superou expectativas')
]
session.add_all(avaliacoes)

session.commit()

print("Banco de dados populado com sucesso!")
print(f"Total de registros:")
print(f"Usuários: {session.query(Usuario).count()}")
print(f"Produtos: {session.query(Produto).count()}")
print(f"Pedidos: {session.query(Pedido).count()}")
print(f"Avaliações: {session.query(Avaliacao).count()}")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario, Produto, Pedido, Avaliacao

engine = create_engine('sqlite:///exercicios.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#order_by()
#16. Liste todos os usuários em ordem alfabética de nome.
# usuarios = session.query(Usuario).order_by(Usuario.nome).all()
# for usuario in usuarios:
#     print(usuario.nome)

#18. Organize os pedidos por data de criação (mais recentes primeiro) e depois por status.
# pedidos = session.query(Pedido).order_by(Pedido.status, Pedido.data_pedido ).all()
# for pedido in pedidos:
#     print(pedido.usuario_id
#     ,pedido.produto_id
#     ,pedido.quantidade
#     ,pedido.status
#     ,pedido.data_pedido)

#19. Liste os 10 primeiros usuários cadastrados no sistema.
# usuarios = session.query(Usuario).limit(5).all()
# for usuario in usuarios:
#     print(usuario)

#22. Liste os usuários cadastrados, ignorando os 5 primeiros resultados.
usuarios = session.query(Usuario).offset(5).all()
for usuario in usuarios:
    print(usuario)
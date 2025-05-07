from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Usuario

engine = create_engine('sqlite:///exemplo.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# População de Usuários
usuarios = [
    Usuario(nome='Antony', email='ant@exemplo.com'),
    Usuario(nome='Jales', email='jal@exemplo.com'),
    Usuario(nome='Lucas', email='luc@exemplo.com'),
    Usuario(nome='Gabriel', email='gab@exemplo.com'),
    Usuario(nome='Beatriz', email='bia@exemplo.com'),
]
session.add_all(usuarios)
session.commit()

# População de Produtos
print("Banco de dados populado com sucesso!")
print(f"Total de registros:")
print(f"Usuários: {session.query(Usuario).count()}")
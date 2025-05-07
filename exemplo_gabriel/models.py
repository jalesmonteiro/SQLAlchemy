from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __str__(self):
        return f"{self.id}, {self.nome}, {self.email}"
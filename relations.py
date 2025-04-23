from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

''' um-para-um '''
class Pessoa(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = relationship("CPF", back_populates="pessoa", uselist=False)

class CPF(Base):
    __tablename__ = 'cpfs'
    id = Column(Integer, primary_key=True)
    numero = Column(String, unique=True)
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship("Pessoa", back_populates="cpf")


''' um-para-muitos '''
class Turma(Base):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    alunos = relationship("Aluno", back_populates="turma")

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    turma_id = Column(Integer, ForeignKey('turmas.id'))
    turma = relationship("Turma", back_populates="alunos")


''' muitos-para-muitos '''
aluno_turma = Table(
    'aluno_turma', Base.metadata,
    Column('aluno_id', Integer, ForeignKey('alunos.id'), primary_key=True),
    Column('turma_id', Integer, ForeignKey('turmas.id'), primary_key=True)
)

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    turmas = relationship("Turma", secondary=aluno_turma, back_populates="alunos")

class Turma(Base):
    __tablename__ = 'turmas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    alunos = relationship("Aluno", secondary=aluno_turma, back_populates="turmas")
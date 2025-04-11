from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(200), nullable=False)
    concluida = Column(Boolean, default=False)

    def concluir(self):
        self.concluida = True

    def reabrir(self):
        self.concluida = False

    def __repr__(self):
        status = "Concluída" if self.concluida else "Não concluída"
        return f"{self.descricao} - {status}"

class ListaDeTarefas:
    def __init__(self, session: Session):
        """Recebe uma sessão SQLAlchemy para gerenciar as tarefas."""
        self.session = session

    def adicionar_tarefa(self, descricao):
        nova_tarefa = Tarefa(descricao=descricao)
        self.session.add(nova_tarefa)
        self.session.commit()

    def remover_tarefa(self, indice):
        tarefa = self._get_tarefa_por_indice(indice)
        if tarefa:
            self.session.delete(tarefa)
            self.session.commit()

    def concluir_tarefa(self, indice):
        tarefa = self._get_tarefa_por_indice(indice)
        if tarefa:
            tarefa.concluir()
            self.session.commit()

    def reabrir_tarefa(self, indice):
        tarefa = self._get_tarefa_por_indice(indice)
        if tarefa:
            tarefa.reabrir()
            self.session.commit()

    def listar_tarefas(self):
        return self.session.query(Tarefa).order_by(Tarefa.id).all()

    def _get_tarefa_por_indice(self, indice):
        tarefas = self.listar_tarefas()
        return tarefas[indice] if indice < len(tarefas) else None
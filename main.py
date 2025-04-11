from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ListaDeTarefas, Tarefa
import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Configuração do banco de dados
    engine = create_engine("sqlite:///tarefas.db")
    Tarefa.__table__.create(bind=engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Cria a lista de tarefas usando a sessão configurada
    lista_de_tarefas = ListaDeTarefas(session)

    # Exemplo de uso
    while True:
        # Exibir lista de tarefas
        tarefas = lista_de_tarefas.listar_tarefas()
        if not tarefas:
            print("\nNão há tarefas.")
        else:
            print("\nTarefas:")
            for indice, tarefa in enumerate(tarefas):
                print(f"{indice}: {tarefa}")

        # Menu
        print("\n1. Adicionar tarefa\n2. Remover tarefa\n3. Concluir tarefa\n4. Reabrir tarefa\n5. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            descricao = input("Digite a descrição da tarefa: ")
            lista_de_tarefas.adicionar_tarefa(descricao)
            print("Tarefa adicionada com sucesso!")
            time.sleep(1)
            limpar_tela()
        elif escolha == '2':
            if not tarefas:
                print("Não há tarefas para remover.")
            else:
                indice = int(input("\nDigite o índice da tarefa para remover: "))
                lista_de_tarefas.remover_tarefa(indice)
                print("Tarefa removida com sucesso!")
                time.sleep(1)
                limpar_tela()
        elif escolha == '3':
            if not tarefas:
                print("Não há tarefas para concluir.")
            else:
                indice = int(input("\nDigite o índice da tarefa para concluir: "))
                lista_de_tarefas.concluir_tarefa(indice)
                print("Tarefa concluída com sucesso!")
                time.sleep(1)
                limpar_tela()
        elif escolha == '4':
            if not tarefas:
                print("Não há tarefas para reabrir.")
            else:
                indice = int(input("\nDigite o índice da tarefa para reabrir: "))
                lista_de_tarefas.reabrir_tarefa(indice)
                print("Tarefa reaberta com sucesso!")
                time.sleep(1)
                limpar_tela()
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")
            time.sleep(1)
            limpar_tela()

if __name__ == "__main__":
    main()
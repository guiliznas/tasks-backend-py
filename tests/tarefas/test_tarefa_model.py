from src.db.models import TarefaModel
from datetime import datetime


def test_calc_prazo():
    tarefa = TarefaModel(**{
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15/12/2022",
        "carga": 1
    })
    prazo_entrega = tarefa.prazo_entrega(today=datetime(2022, 12, 10))
    assert prazo_entrega == 40

    tarefa = TarefaModel(**{
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15/12/2022",
        "carga": 1
    })
    prazo_entrega = tarefa.prazo_entrega(today=datetime(2022, 12, 15))
    assert prazo_entrega == 0

    tarefa = TarefaModel(**{
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15/12/2022",
        "carga": 1
    })
    prazo_entrega = tarefa.prazo_entrega(today=datetime(2022, 12, 16))
    assert prazo_entrega == -8

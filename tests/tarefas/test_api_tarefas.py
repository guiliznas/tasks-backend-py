from src.api.APITask import APITask


def test_can_create_task(client):
    tarefa = {
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15-12-2022",
        "carga": 1
    }

    res = client.post('/tarefas', json=tarefa)

    assert res.status_code == 201

    data = res.json

    assert data['titulo'] == tarefa['titulo']
    assert data['descricao'] == tarefa['descricao']
    assert data['importancia'] == tarefa['importancia']
    assert data['urgencia'] == tarefa['urgencia']
    assert data['carga'] == tarefa['carga']
    assert data['prazo'] == '15/12/2022'
    assert data.get('id')


def test_can_update_task(client):
    tarefa = {
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15-12-2022",
        "carga": 1
    }
    res = client.post('/tarefas', json=tarefa)
    tarefa = res.json
    res = client.put("/tarefa/{}".format(tarefa['id']), json={"titulo": "titulo atualizado"})
    assert res.status_code == 200
    data = res.json
    assert data['titulo'] == "titulo atualizado"


def test_can_remove_task(client):
    tarefa = {
        "titulo": "Teste de tarefa",
        "descricao": "Criando a primeira tarefa do servidor",
        "importancia": 10,
        "urgencia": 10,
        "prazo": "15-12-2022",
        "carga": 1
    }
    res = client.post('/tarefas', json=tarefa)
    tarefa = res.json

    res = client.delete('/tarefa/{}'.format(tarefa['id']))

    assert res.status_code == 200

    tarefas = client.get('/tarefas')
    tarefas = tarefas.json
    ids = [x['id'] for x in tarefas]
    assert tarefa['id'] not in ids

    res = client.get('/tarefa/{}'.format(tarefa['id']))
    assert res.status_code == 404
    data = res.json
    assert data['message'] == 'Tarefa não encontrada'

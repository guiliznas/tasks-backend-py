from flask import request
from flask_restful import Resource, reqparse

from src.db.models import TarefaModel, db

parser_post = reqparse.RequestParser()
parser_post.add_argument('titulo',
                         type=str,
                         required=True,
                         help="Valor não pode ser nulo",
                         )
parser_post.add_argument('descricao',
                         type=str
                         )
parser_post.add_argument('importancia',
                         type=float,
                         )
parser_post.add_argument('urgencia',
                         type=float
                         )
parser_post.add_argument('prazo',
                         )
parser_post.add_argument('carga',
                         type=float,
                         )


class TasksListResource(Resource):
    def get(self):
        tarefas = TarefaModel.query.all()
        return list(x.json() for x in tarefas)

    def post(self):
        # data = request.get_json()
        data = parser_post.parse_args()
        tarefa = TarefaModel(data['titulo'], data['descricao'], data['importancia'], data['urgencia'], data['prazo'],
                             data['carga'])
        db.session.add(tarefa)
        db.session.flush()
        db.session.commit()
        return tarefa.json(), 201

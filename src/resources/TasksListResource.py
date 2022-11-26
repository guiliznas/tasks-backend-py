from flask import request
from flask_restful import Resource, reqparse

from src.api.APITask import APITask
from src.db.models import TarefaModel, db
from src.utils import flask_requests_parser

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
                         type=flask_requests_parser.parser_date_dayfirst_v2,
                         )
parser_post.add_argument('carga',
                         type=float,
                         )


class TasksListResource(Resource):
    def get(self, ):
        modo = request.args.get('modo')
        # tarefas = TarefaModel.query.all()
        # return list(x.json() for x in tarefas)
        api = APITask()
        return api.listar(modo=modo)

    def post(self):
        # data = request.get_json()
        data = parser_post.parse_args()

        api = APITask()
        tarefa, status_code = api.salvar(data=data)
        # tarefa = TarefaModel(data['titulo'], data['descricao'], data['importancia'], data['urgencia'], data['prazo'],
        #                      data['carga'])
        # db.session.add(tarefa)
        # db.session.flush()
        # db.session.commit()
        return tarefa, status_code

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
        agenda = request.args.get('agenda')
        modo = request.args.get('modo')
        ativas = request.args.get('ativas', False)
        # tarefas = TarefaModel.query.all()
        # return list(x.json() for x in tarefas)
        api = APITask()
        return api.listar(modo=modo, agenda=agenda, ativas=ativas)

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

    def put(self):
        from src.tester import Tester
        from src.db.models import TarefaModel
        sheet_name = request.args.get('sheet', 'semana2')
        t = Tester()
        df = t._read_mock(sheet_name=sheet_name)
        df = df.rename(columns={
            'Titulo': 'titulo',
            'Importância': 'importancia',
            'Urgência': 'urgencia',
            'Data entrega': 'prazo',
            'Carga': 'carga'
        })
        df = df[[
            'titulo',
            'importancia',
            'urgencia',
            'prazo',
            'carga'
        ]]
        df['descricao'] = ''
        api = APITask()
        for task in df.to_dict(orient='records'):
            tarefa = (TarefaModel(**task))
            print(tarefa)
            api.salvar(data=task)

    def delete(self):
        return TarefaModel.query().delete()

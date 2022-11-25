from flask import request
from flask_restful import Resource, reqparse

from src.db.models import TarefaModel, db
from src.utils import flask_requests_parser

parser_put = reqparse.RequestParser()
parser_put.add_argument('titulo',
                        type=str,
                        )
parser_put.add_argument('descricao',
                        type=str
                        )
parser_put.add_argument('importancia',
                        type=float,
                        )
parser_put.add_argument('urgencia',
                        type=float
                        )
parser_put.add_argument('prazo',
                        type=flask_requests_parser.parser_date_dayfirst_v2,
                        )
parser_put.add_argument('carga',
                        type=float,
                        )


class TaskResource(Resource):
    def get(self, id):
        tarefa = TarefaModel.query.filter_by(id=id).first()
        if tarefa:
            return tarefa.json()
        return {'message': 'Tarefa não encontrada'}, 404

    def put(self, id):
        # data = request.get_json()
        data = parser_put.parse_args()

        tarefa = TarefaModel.query.filter_by(id=id).first()

        if tarefa:
            tarefa.titulo = data['titulo']
            tarefa.descricao = data['descricao']
            tarefa.importancia = data['importancia']
            tarefa.urgencia = data['urgencia']
            tarefa.prazo = data['prazo']
            tarefa.carga = data['carga']
        else:
            tarefa = TarefaModel(**data)

        db.session.add(tarefa)
        db.session.flush()
        db.session.commit()

        return tarefa.json()

    def delete(self, id):
        tarefa = TarefaModel.query.filter_by(id=id).first()

        if tarefa:
            db.session.delete(tarefa)
            db.session.commit()

            return {'message': 'Tarefa removida'}

        return {'message': 'Tarefa não encontrada'}, 404

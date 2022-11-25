from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP
import uuid

from src.utils import tratamento_datas

db = SQLAlchemy()


class TarefaModel(db.Model):
    __tablename__ = "tarefa"

    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    titulo = db.Column(db.String())
    descricao = db.Column(db.String())
    importancia = db.Column(db.Float())
    urgencia = db.Column(db.Float())
    prazo = db.Column(TIMESTAMP)
    carga = db.Column(db.Float())

    def __init__(self,
                 titulo,
                 descricao,
                 importancia,
                 urgencia,
                 prazo,
                 carga,
                 ):
        self.titulo = titulo
        self.descricao = descricao
        self.importancia = importancia
        self.urgencia = urgencia
        self.prazo = prazo
        self.carga = carga

    def json(self):
        print(type(self.prazo))
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "importancia": self.importancia,
            "urgencia": self.urgencia,
            "prazo": tratamento_datas.convert_datetime_to_str(self.prazo) if self.prazo else None,
            "carga": self.carga,
        }

    def __repr__(self):
        return f"{self.titulo}"

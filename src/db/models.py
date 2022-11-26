from sqlalchemy import TIMESTAMP
import uuid

from src.utils import tratamento_datas

from src.db.database import db
from datetime import datetime
import pandas as pd


class TarefaModel(db.Model):
    __tablename__ = "tarefa"

    id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    titulo = db.Column(db.String())
    descricao = db.Column(db.String())
    importancia = db.Column(db.Float())
    urgencia = db.Column(db.Float())
    prazo = db.Column(db.DateTime)
    carga = db.Column(db.Float())

    peso_sem_modelo = db.Column(db.Float())
    peso_basico = db.Column(db.Float())
    peso_avancado = db.Column(db.Float())
    peso_alternativo = db.Column(db.Float())

    def prazo_entrega(self, today=None) -> int:
        if not self.prazo:
            return None
        if not today:
            today = datetime.today().date()
        _format = '%d/%m/%Y'
        data_entrega = self.prazo
        if isinstance(data_entrega, float):
            data_entrega = datetime.fromtimestamp(data_entrega)
        if isinstance(data_entrega, datetime):
            data_entrega = data_entrega.date()
        if isinstance(data_entrega, str):
            data_entrega = datetime.strptime(self.prazo, _format)
        diff = data_entrega - today
        # TODO: Pegar o horario por dia do user
        return diff.days * 8

    def __init__(self,
                 titulo,
                 descricao,
                 importancia,
                 urgencia,
                 prazo,
                 carga,
                 id=None,
                 peso_sem_modelo=None,
                 peso_basico=None,
                 peso_avancado=None,
                 peso_alternativo=None,
                 prazo_entrega=None,  ## nao usar
                 carga_prazo=None,
                 ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.importancia = importancia
        self.urgencia = urgencia
        self.prazo = prazo
        self.carga = carga
        self.peso_sem_modelo = peso_sem_modelo
        self.peso_basico = peso_basico
        self.peso_avancado = peso_avancado
        self.peso_alternativo = peso_alternativo

    def json(self):
        import datetime as d
        prazo = tratamento_datas.convert_datetime_to_str(self.prazo) if self.prazo else None
        if type(prazo) is d.date:
            prazo = prazo.strftime("%d/%m/%Y")
        print("JSON", type(prazo))
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "importancia": self.importancia,
            "urgencia": self.urgencia,
            "prazo": prazo,
            "prazo_entrega": self.prazo_entrega(),
            "carga": self.carga,
            "peso_sem_modelo": self.peso_sem_modelo,
            "peso_basico": self.peso_basico,
            "peso_avancado": self.peso_avancado,
            "peso_alternativo": self.peso_alternativo,
        }

    def __repr__(self):
        return f"{self.titulo}"

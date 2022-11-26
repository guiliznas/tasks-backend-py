from src.db.models import TarefaModel
from src.db.database import db
from src.core.otimizador import Otimizador
import pandas as pd
from datetime import datetime

from src.utils import tratamento_datas


class APITask:
    def __init__(self, user=None, session=None):
        if user is None:
            user = {'modelo': 'alternativo'}
        self.user = user

        self.session = session or db.session
        self.otimizador = Otimizador()

    def _calcular_pesos(self, tarefa: TarefaModel):

        dic = tarefa.json()
        # dic['prazo_entrega'] = tarefa.prazo_entrega()

        if not dic['prazo_entrega']:
            return tarefa

        dic['peso_sem_modelo'] = self.otimizador.sem_modelo(tarefa=dic)
        dic['peso_basico'] = self.otimizador.basico(tarefa=dic)
        dic['peso_avancado'] = self.otimizador.avancado(tarefa=dic)
        dic['peso_alternativo'] = self.otimizador.alternativo(tarefa=dic)

        return TarefaModel(**dic)

    def salvar(self, data: dict, id: str = None):
        # TODO: se a tarefa tiver id e nao encontrar, retornar status 404
        tarefa = None
        if id:
            tarefa = TarefaModel.query.filter_by(id=id).first()
            if not tarefa:
                return {'message': 'Tarefa não encontrada'}, 404

        status_code = 200 if id else 201

        if tarefa:
            tarefa.titulo = data['titulo']
            tarefa.descricao = data['descricao']
            tarefa.importancia = data['importancia']
            tarefa.urgencia = data['urgencia']
            # prazo = pd.Timestamp(data['prazo']).to_datetime()
            prazo = datetime.fromisoformat(data['prazo'].isoformat())
            # tarefa.prazo = data['prazo']
            tarefa.prazo = prazo.date()
            tarefa.carga = data['carga']
        else:
            tarefa = TarefaModel(**data)

        tarefa = self._calcular_pesos(tarefa=tarefa)

        print("Tipo", type(tarefa.prazo))
        if isinstance(tarefa.prazo, str):
            tarefa.prazo = tratamento_datas.parse_to_datetime(tarefa.prazo)

        print("Tarefa", tarefa.json())

        if id:
            self.session.merge(tarefa)
        else:
            self.session.add(tarefa)
        self.session.flush()
        self.session.commit()

        return tarefa.json(), status_code

    def remover(self, id: str):

        tarefa = TarefaModel.query.filter_by(id=id).first()

        if tarefa:
            self.session.delete(tarefa)
            self.session.commit()

            return {'message': 'Tarefa removida'}, 200

        return {'message': "Tarefa não encontrada"}, 404

    def listar(self, modo='alternativo'):
        if modo not in ['sem_modelo', 'basico', 'avancado', 'alternativo']:
            modo = 'alternativo'
        tarefas = TarefaModel.query.all()
        df = pd.DataFrame(list(x.json() for x in tarefas))
        # TODO: Considerar modo do user
        if len(df) == 0:
            return []
        return df.sort_values('peso_{}'.format(modo), ascending=False).to_dict(orient='records')

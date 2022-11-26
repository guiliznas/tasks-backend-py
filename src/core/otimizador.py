from src.config import COLUMNS


class Otimizador:
    def __init__(self, mode='full'):
        self.mode = mode

    def run(self, df, mode=None):
        if not mode:
            mode = self.mode

        MAP_FUNCS = {
            'full': self._full,
            'alternative': self._alternative,
            'partial': self._partial,
            'dumb': self._dumb,
        }

        func = MAP_FUNCS[mode]
        if func:
            return func(df)

        return df

    def sem_modelo(self, tarefa: dict, arg="urgencia"):
        tarefa = tarefa.copy()
        tarefa['peso_sem_modelo'] = tarefa[arg]
        return tarefa['peso_sem_modelo']

    def _dumb(self, df_old, arg="Urgência"):
        tasks = df_old.copy()
        tasks['peso'] = tasks.loc[:, arg]
        return tasks

    def basico(self, tarefa: dict):
        tarefa = tarefa.copy()
        tarefa['urgencia'] = tarefa['carga'] / tarefa['prazo_entrega']
        tarefa['peso_basico'] = 2 * tarefa['urgencia'] + tarefa['importancia']
        return tarefa['peso_basico']

    def _partial(self, df_old):
        df = df_old.copy()
        tasks = df.loc[:, COLUMNS].copy()
        tasks.loc[:, 'Urgência'] = tasks['Carga'] / tasks['Prazo Entrega']
        tasks['peso'] = 2 * tasks.loc[:, 'Urgência'] + tasks.loc[:, 'Importância']
        return tasks

    def avancado(self, tarefa: dict):
        tarefa = tarefa.copy()
        tarefa['carga_prazo'] = tarefa['carga'] / tarefa['prazo_entrega'] * 15
        tarefa['peso_avancado'] = (2 * tarefa['urgencia'] + tarefa['importancia']) / tarefa['carga_prazo']
        if tarefa['carga_prazo'] <= 1:
            tarefa['peso_avancado'] = tarefa['peso_avancado'] + tarefa['carga_prazo'] * 100
        return tarefa['peso_avancado']

    def _full(self, df_old):
        df = df_old.copy()
        tasks = df.loc[:, COLUMNS].copy()

        # tarefas com carga_prazo > 1 não serão entregues antes do prazo
        tasks['carga_prazo'] = tasks['Carga'] / tasks['Prazo Entrega'] * 15

        # se dividir, vai mostrar quantos pontos de peso tem em cada unidade de prazo
        tasks['peso'] = (2 * tasks['Urgência'] + tasks['Importância']) / tasks['carga_prazo']
        # Se a carga_prazo for maior que 1, a tarefa está teoricamente atrasada
        for i, row in tasks.iterrows():
            if (row['carga_prazo'] <= 1):
                tasks.loc[i, 'peso'] = row['peso'] + row['carga_prazo'] * 100
        return tasks

    def alternativo(self, tarefa):
        tarefa = tarefa.copy()
        tarefa['carga_prazo'] = (tarefa['carga'] / tarefa['prazo_entrega']) * 15
        tarefa['urgencia'] = tarefa['carga_prazo']
        tarefa['peso_alternativo'] = (4 * tarefa['urgencia'] + tarefa['importancia']) / tarefa['carga_prazo']
        if tarefa['carga_prazo'] <= 1:
            tarefa['peso_alternativo'] = tarefa['peso_alternativo'] + tarefa['carga_prazo'] * 10
        return tarefa['peso_alternativo']

    def _alternative(self, df_old):
        df = df_old.copy()
        tasks = df.loc[:, COLUMNS].copy()

        tasks['carga_prazo'] = (tasks['Carga'] / tasks['Prazo Entrega']) * 15

        # Considerar mais urgente aquilo que possui menos tempo para ser concluído
        tasks['Urgência'] = tasks['carga_prazo']

        tasks['peso'] = (4 * tasks['Urgência'] + tasks['Importância']) / tasks['carga_prazo']
        for i, row in tasks.iterrows():
            if (row['carga_prazo'] <= 1):
                tasks.loc[i, 'peso'] = row['peso'] + row['carga_prazo'] * 10
        return tasks

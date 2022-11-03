from .utils import format_to_number
from .config import COLUMNS

class Otimizador:
  def __init__(self):
    return

  def dumb_mode(self, df_old, arg="Importância"):
    tasks = df_old.copy()
    tasks['peso'] = tasks.loc[:, arg]
    return tasks

  def simple(self, df_old):
    df = df_old.copy()
    tasks = df.loc[:,COLUMNS].copy()
    tasks.loc[:, 'Urgência'] = tasks['Carga'] / tasks['Prazo Entrega']
    tasks['peso'] = 2 * tasks.loc[:,'Urgência'] + tasks.loc[:,'Importância']
    return tasks

  def second(self, df_old):
    df = df_old.copy()
    tasks = df.loc[:,COLUMNS].copy()
    
    # tarefas com carga_prazo > 1 não serão entregues antes do prazo
    tasks['carga_prazo'] = tasks['Carga'] / tasks['Prazo Entrega']*15
    # campo de urgencia deveria ser a relação de carga e prazo?
    # tasks['Urgência'] = tasks['carga_prazo'] * 10
    
    # se dividir vai dizer qnts pontos de peso tem em cada unidade de prazo?
    tasks['peso'] = (2 * tasks['Urgência'] + tasks['Importância']) / tasks['carga_prazo']
    # Se a carga_prazo for maior q 1 não é melhor deixar para depois?
    # breakpoint()
    for i, row in tasks.iterrows():
      if (row['carga_prazo'] <= 1):
        # tasks.loc[i, 'peso'] = row['peso'] *10 + row['carga_prazo']*100 # + row['Carga']
        tasks.loc[i, 'peso'] = row['peso'] + row['carga_prazo']*100 # + row['Carga']

    def second_old(self):
      df = df_old.copy()
      tasks = df.loc[:,['Titulo', 'Importância', 'Urgência', 'Carga', 'Prazo Entrega']].copy()
      
      # tarefas com carga_prazo > 1 não serão entregues antes do prazo
      tasks['carga_prazo'] = tasks['Carga'] / tasks['Prazo Entrega']
      tasks['Urgência'] = (tasks['Carga'] / tasks['Prazo Entrega']) * 10
      
      # tasks['peso'] = (1.5*tasks['Urgência']+tasks['Importância'])* tasks['carga_prazo']
      # se dividir vai dizer qnts pontos de peso tem em cada unidade de prazo?
      # tasks['peso'] = (2 * tasks['Urgência'] + tasks['Importância']) / tasks['carga_prazo']
      # Se a carga_prazo for maior q 1 não é melhor deixar para depois?
      tasks['peso'] = (2 * tasks['Urgência'] + tasks['Importância']) / tasks['carga_prazo']
      # tasks['peso'] = tasks['peso'].apply(lambda x: int(x) * 10)
      # tasks['peso'] = tasks.apply(lambda x: x['peso'] if x['carga_prazo'] > 1 else x['peso'] + x['carga_prazo'])
      for i, row in tasks.iterrows():
        if (row['carga_prazo'] <= 1):
          tasks.loc[i, 'peso'] = row['peso'] + row['Carga'] # + row['carga_prazo']

    return tasks
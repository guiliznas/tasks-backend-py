from .utils import format_to_number

class Otimizador:
  def __init__(self):
    return

  def dumb_mode(self, df_old, arg="Importância"):
    df = df_old.copy()
    tasks = df.copy()
    tasks = format_to_number(tasks)
    # tasks.loc[:,'Importância'] = pd.to_numeric(tasks['Importância'], errors='coerce')
    # tasks.loc[:,'Urgência'] = pd.to_numeric(tasks.loc[:,'Urgência'], errors='coerce')
    tasks['peso'] = tasks.loc[:, arg]
    return tasks

  def simple(self, df_old):
    df = df_old.copy()
    tasks = df.loc[:,['Titulo', 'Importância', 'Urgência', 'Carga', 'Prazo Entrega']].copy()
    tasks = format_to_number(tasks)
    # tasks.loc[:,'Importância'] = pd.to_numeric(tasks.loc[:, 'Importância'], errors='coerce')
    # tasks.loc[:,'Carga'] = pd.to_numeric(tasks['Carga'], errors='coerce')
    # tasks.loc[:,'Prazo Entrega'] = pd.to_numeric(tasks['Prazo Entrega'], errors='coerce')
    # tasks.loc[:,'Urgência'] = pd.to_numeric(tasks.loc[:,'Urgência'], errors='coerce')
    tasks.loc[:, 'Urgência'] = tasks['Carga'] / tasks['Prazo Entrega']
    tasks['peso'] = 2 * tasks.loc[:,'Urgência'] + tasks.loc[:,'Importância']
    return tasks

  def second(self, df_old):
    df = df_old.copy()
    tasks = df.loc[:,['Titulo', 'Importância', 'Urgência', 'Carga', 'Prazo Entrega']].copy()
    tasks = format_to_number(tasks)
    # tasks.loc[:,'Importância'] = pd.to_numeric(tasks['Importância'], errors='coerce')
    # tasks.loc[:,'Urgência'] = pd.to_numeric(tasks['Urgência'], errors='coerce')
    # tasks.loc[:,'Carga'] = pd.to_numeric(tasks['Carga'], errors='coerce')
    # tasks.loc[:,'Prazo Entrega'] = pd.to_numeric(tasks['Prazo Entrega'], errors='coerce')
    
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

    # campo de urgencia deveria ser a relação de carga e prazo?

    return tasks
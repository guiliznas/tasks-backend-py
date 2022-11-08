from .otimizador import Otimizador
from .utils import format_to_number, sorter, random_value

import pandas as pd
import json

class Tester:
  def __init__(self):
    self.otimizador = Otimizador()
  
  def _random_tasks(self, size=40):
    # from random import seed
    
    columns = ['Titulo', 'Importância', 'Urgência', 'Carga', 'Prazo Entrega']

    df = pd.DataFrame(columns=columns)
    lista = list()
    for i in range(size):
      carga = random_value(min=1, max=5)
      prazo = random_value(min=1, max=7)*8
      # df = df.append({
      #     'Titulo': i,
      #     'Importância': random_value(),
      #     'Urgência': carga / prazo * 100,
      #     'Carga': carga,
      #     'Prazo Entrega': prazo,
      # }, ignore_index=True)
      lista.append({
          'Titulo': i,
          'Importância': random_value(),
          'Urgência': carga / prazo * 100,
          'Carga': carga,
          'Prazo Entrega': prazo,
      })
    # # seed random number generator
    # seed(1)
    df = pd.DataFrame.from_records(lista)
    return df

  def _read_mock(self, sheet_name='semana2'):
    df = pd.read_excel('src/mock/Tarefas.xlsx', sheet_name=sheet_name)
    df = format_to_number(df)
    return df

  def calc_done(self, df_old):
    df = df_old.copy()
    total = 0

    dt = df.copy(deep=True)

    for i, row in dt.iterrows():
      total += row['Carga']
      dt.loc[i, 'done_in'] = total

    return dt

  def calc_success(self, df_old):
    df = df_old.copy()
    df['success'] = df['Prazo Entrega'] > df['done_in']

    return df
  
  def calc_diff_time(self, df_old):
    df = df_old.copy()

    dt = df.copy()

    dt['free_time'] = dt['Prazo Entrega'] - dt['done_in']

    return dt

  def calc_stats(self, df_old, name):
    df = df_old.copy()
    data = {
        name: {
            # 'success': "{0:.2f}%".format(df['success'].sum() / len(df) * 100),
            'success': df['success'].sum() / len(df) * 100,
            # 'free_time': "{0:.0f}h".format(df['free_time'].sum()),
            'free_time': df['free_time'].sum()
        }
    }

    dt = pd.DataFrame(data)

    return dt.T

  def calc_results(self, df):
    df_dumb = sorter(self.otimizador.run(df.copy(deep=True), 'dumb'))
    df_simple = sorter(self.otimizador.run(df.copy(deep=True), 'partial'))
    df_complex = sorter(self.otimizador.run(df.copy(deep=True), 'full'))
    df_complex_2 = sorter(self.otimizador.run(df.copy(deep=True), 'alternative'))
    dfs = [
        {
          'name': 'default',
          'value': df.copy(deep=True),
        },
        {
            'name': 'dumb',
            'value': df_dumb
        },
        {
            'name': 'simple',
            'value': df_simple,
        },
        {
            'name': 'complex',
            'value': df_complex,
        },
        {
          'name': 'complex2',
          'value': df_complex_2
        }
    ]

    df_result = pd.DataFrame(columns=['free_time', 'success'])
    for item in dfs:
      item['value'] = self.calc_done(item['value'])
      item['value'] = self.calc_success(item['value'])
      item['value'] = self.calc_diff_time(item['value'])
      df_result.loc[item['name']] = self.calc_stats(item['value'], item['name']).loc[item['name']]

    return df_result

  def run(self):
    sheets = [
      'teste base',
      'trabalho',
      'pessoal',
      'semana1',
      'semana2'
    ]
    for sheet in sheets:
      df = self._read_mock(sheet_name=sheet)

      result = self.calc_results(df)
      result = result.sort_values(['success', 'free_time'], ascending=[False, False])
      result['free_time'] = result['free_time'].map(lambda x: "{0:.0f}h".format(x))
      result['success'] = result['success'].map(lambda x: "{0:.1f}%".format(x))
      print("\n" + sheet)
      print(result)
      print('\n')
    return True

  def run_random(self):
    df = self._random_tasks()
    with open('data.json', 'w+') as file:
      file.write(df.to_json(orient='records'))
    result = self.calc_results(df)
    result = result.sort_values(['success', 'free_time'], ascending=[False, False])
    result['free_time'] = result['free_time'].map(lambda x: "{0:.0f}h".format(x))
    result['success'] = result['success'].map(lambda x: "{0:.1f}%".format(x))
    print(result)

  def run_batch(self, size=100):
    import sys
    # def start_progress(title):
    #   global progress_x
    #   sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    #   sys.stdout.flush()
    #   progress_x = 0

    # def progress(x):
    #   global progress_x
    #   x = int(x * 40 // 100)
    #   sys.stdout.write("#" * (x - progress_x))
    #   sys.stdout.flush()
    #   progress_x = x

    # def end_progress():
    #   sys.stdout.write("#" * (40 - progress_x) + "]\n")
    #   sys.stdout.flush()
    
    # start_progress('Simulando')
    free_time = dict()
    success = dict()
    both = dict()
    dfs = []
    for i in range(size):
      # progress(i)
      df = self._random_tasks()
      dfs.append(df.to_dict(orient='records'))
      result = self.calc_results(df)
      max_free_time = result['free_time'].idxmax()
      max_success = result['success'].idxmax()
      if max_free_time in free_time:
        free_time[max_free_time] += 1
      else:
        free_time[max_free_time] = 1
      if max_success in success:
        success[max_success] += 1
      else:
        success[max_success] = 1
      if max_free_time == max_success:
        if max_free_time in both:
          both[max_free_time] += 1
        else:
          both[max_free_time] = 1

    with open('datas.json', 'w+') as file:
      file.write(json.dumps(dfs))

    # end_progress()
    free_time = {k: v for k, v in sorted(free_time.items(), key=lambda item: item[1], reverse=True)}
    print('free_time', free_time)
    success = {k: v for k, v in sorted(success.items(), key=lambda item: item[1], reverse=True)}
    print('success', success)
    both = {k: v for k, v in sorted(both.items(), key=lambda item: item[1], reverse=True)}
    print('both', both)
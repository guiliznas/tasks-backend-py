import pandas as pd
from random import random

def format_to_number(df_old):
  df = df_old.copy(deep=True)
  columns = ['Importância', 'Carga', 'Prazo Entrega', 'Urgência']
  for column in columns:
    if column in df.columns:
      df.loc[:, column] = pd.to_numeric(df[column], errors='coerce')
  return df

def sorter(df_old):
  df = df_old.copy()
  return df.copy().sort_values('peso', ascending=False)

def random_value(min=0, max=10):
  return abs(int(min + (random() * (max - min))))
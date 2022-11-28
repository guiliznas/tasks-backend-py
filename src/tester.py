from src.core.otimizador import Otimizador
from src.utils_funcs import format_to_number, sorter, random_value

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
            prazo = random_value(min=5, max=10) * 8
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

    def calc_gain(self, df_old):
        df = df_old.copy()
        df['gain_success'] = (df['success'] / df.loc['default', 'success']) - 1
        if df.loc['default', 'free_time'] != 0:
            if df.loc['default', 'free_time'] < 0:
                free = abs(df.loc['default', 'free_time'])
                df['gain_free_time'] = (df['free_time'] + free) / free
            else:
                free = df.loc['default', 'free_time']
                df['gain_free_time'] = (df['free_time'] - free) / free
        else:
            df['gain_free_time'] = 0
        return df

    def calc_results(self, df):
        df_dumb = sorter(self.otimizador.run(df.copy(deep=True), 'dumb'))
        df_simple = sorter(self.otimizador.run(df.copy(deep=True), 'partial'))
        df_full = sorter(self.otimizador.run(df.copy(deep=True), 'full'))
        df_alternative = sorter(self.otimizador.run(df.copy(deep=True), 'alternative'))
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
                'name': 'full',
                'value': df_full,
            },
            {
                'name': 'alternative',
                'value': df_alternative
            }
        ]

        df_result = pd.DataFrame(columns=['free_time', 'success'])
        for item in dfs:
            item['value'] = self.calc_done(item['value'])
            item['value'] = self.calc_success(item['value'])
            item['value'] = self.calc_diff_time(item['value'])
            df_result.loc[item['name']] = self.calc_stats(item['value'], item['name']).loc[item['name']]

        df_result = self.calc_gain(df_result)

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
        def start_progress(title):
            global progress_x
            sys.stdout.write(title + ": [" + "-" * 40 + "]" + chr(8) * 41)
            sys.stdout.flush()
            progress_x = 0

        def progress(x):
            global progress_x
            x = int(x * 40 // 100)
            sys.stdout.write("#" * (x - progress_x))
            sys.stdout.flush()
            progress_x = x

        def end_progress():
            sys.stdout.write("#" * (40 - progress_x) + "]\n")
            sys.stdout.flush()

        def plus_key(counter, key, value=1):
            if key in counter:
                counter[key] = counter[key] + value
            else:
                counter[key] = value

        start_progress('Simulando')
        free_time = dict()
        success = dict()
        both = dict()
        gain_free_time = dict()
        gain_success = dict()
        dfs = []
        results = []
        for i in range(size):
            progress((i / size) * 100)
            df = self._random_tasks()
            dfs.append(df.to_dict(orient='records'))
            result = self.calc_results(df)
            results.append(result.to_dict(orient='index'))
            # max_free_time = result['free_time'].idxmax()
            list_free_times = result[result['free_time'] == result['free_time'].max()].index
            # max_success = result['success'].idxmax()
            list_success = result[result['success'] == result['success'].max()].index
            list_all = result.index
            for i in list_success:
                plus_key(success, i)
                # plus_key(gain_success, i, result.loc[i, 'gain_success'])
            for i in list_free_times:
                plus_key(free_time, i)
                # plus_key(gain_free_time, i, result.loc[i, 'gain_free_time'])
            for i in list(set(list_success) & set(list_free_times)):
                plus_key(both, i)

            for i in list_all:
                plus_key(gain_success, i, result.loc[i, 'gain_success'] or 0)
                plus_key(gain_free_time, i, result.loc[i, 'gain_free_time'] or 0)

        with open('datas.json', 'w+') as file:
            file.write(json.dumps(dfs))

        with open('stats_results.json', 'w+') as file:
            file.write(json.dumps(results))

        end_progress()

        from pprint import pprint

        free_time = {k: v for k, v in sorted(free_time.items(), key=lambda item: item[1], reverse=True)}
        print("\n****Free time****")
        pprint(free_time)
        free_time_gain = {k: v / size for k, v in gain_free_time.items()}
        pprint(free_time_gain)
        print("\n****Success****")
        success = {k: v for k, v in sorted(success.items(), key=lambda item: item[1], reverse=True)}
        pprint(success)
        success_gain = {k: v / size for k, v in gain_success.items()}
        pprint(success_gain)
        print('\n**** Both ****')
        both = {k: v for k, v in sorted(both.items(), key=lambda item: item[1], reverse=True)}
        pprint(both)

        s = f"""
**** Free Time ****
{json.dumps(free_time, indent=1)}
{json.dumps(free_time_gain, indent=1)}

**** Success ****
{json.dumps(success, indent=1)}
{json.dumps(success_gain, indent=1)}

**** Both ****
{json.dumps(both, indent=1)}
    """

        with open('result_batch.txt', 'w+') as file:
            # file.write('**** Free time **** ')
            # file.write(json.dumps(free_time, indent=1))
            # file.write(json.dumps(free_time_gain, indent=1))

            # file.write(json.dumps(success, indent=1))
            # file.write(json.dumps(success_gain, indent=1))

            # file.write(json.dumps(both,indent=1))
            file.write(s)

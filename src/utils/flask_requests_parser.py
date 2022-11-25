import datetime
from src.utils import tratamento_datas
import logging


def parser_date_dayfirst_v2(data):
    try:
        if isinstance(data, (datetime.date, datetime.datetime)):
            return data
        if data == 'null':
            data = None
        if not data:
            raise ValueError(f"Tipo de dado '{data}' ({type(data)}) inválida. Valor esperado: Data no formato %d-%m-%Y")
        _data_parsed = tratamento_datas.parse_date_by_datetime_format_2(data, dayfirst=True)
        if _data_parsed:
            return _data_parsed
        else:
            raise ValueError(f"Data '{data}' inválido. Valor esperado: Data no formato %d-%m-%Y")
    except ValueError as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise ValueError(f"Tipo de dado {data} ({type(data)}) inválido. Valor esperado: Data no formato %d-%m-%Y")

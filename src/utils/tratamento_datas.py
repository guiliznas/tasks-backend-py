import logging
import datetime
import pandas as pd


def parse_date_by_datetime_format_2(x, dayfirst=False):
    """
        if dayfirst:
            _format = '%d-%m-%Y'
        else:
            _format = '%m-%d-%Y'
    :param x:
    :param dayfirst:
    :return:
    """
    try:
        if dayfirst:
            _format = '%d-%m-%Y'
        else:
            _format = '%Y-%m-%d'
        x = datetime.datetime.strptime(x, _format)
        return x.date()
    except Exception as e:
        logging.warning(e)
        return None


def parte_to_datetime(x):
    x = pd.to_datetime(x, dayfirst=True)
    return x.date()


def convert_datetime_to_date(date: datetime.datetime) -> datetime.date:
    if isinstance(date, datetime.datetime):
        return date.date()
    return date


def convert_datetime_to_str(date: datetime.datetime) -> str:
    if isinstance(date, datetime.datetime):
        return date.strftime("%d/%m/%Y %H:%M:%S")
    return date

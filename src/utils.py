from __future__ import annotations

import datetime
import re
import unicodedata
from datetime import date


def normalize_date(d: datetime.datetime | str) -> date:
    """Normalize date strings mixed with Japanese and Western representation. Sometimes, they are ill-formatted.

    Example: '令和４年8月１1' -> '2022-08-11'
    """
    if type(d) is datetime.datetime:
        return d.date()

    if type(d) is str:
        if '令和' in d:
            d = unicodedata.normalize('NFKC', d)
            regex = re.compile(r'.*令和(?P<year>\d+)年\s*(?P<month>\d+)月\s*(?P<day>\d+)日?.*')
            m = regex.match(d)
            return datetime.date(year=int(m['year']) + 2018, month=int(m['month']), day=int(m['day']))
        if '/' in d:
            d = unicodedata.normalize('NFKC', d)
            regex = re.compile(r'.*?(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+).*?')
            m = regex.match(d)
            return datetime.date(year=int(m['year']), month=int(m['month']), day=int(m['day']))

    raise ValueError('date is unexpected value')


def normalize_test_type(availability: str) -> bool:
    """Convert '○' or null to a boolean value."""
    if availability in ['○', '〇']:
        return True
    return False


def convert_excel_date_number(date_num: int) -> date:
    """It looks like Excel default date system starts with 1900-01-01 as `1`."""
    return datetime.date.fromisoformat('1899-12-30')+datetime.timedelta(days=date_num)

# Chiba: fetch the latest Excel data and save it as CSV file
from __future__ import annotations

import datetime
import re
import unicodedata
from datetime import date

import bs4
import pandas as pd
import requests

DOMAIN = 'https://www.pref.chiba.lg.jp'
WEBSITE_URL = f'{DOMAIN}/shippei/kansenshou/pcrmuryouka.html'


def main():
    url = get_latest_excel_url()
    df = pd.read_excel(url, skiprows=4, index_col='NO', dtype={'事業者種別': str})[1:]
    df.index = df.index.astype(int)
    df.rename(columns={'実施検査': 'PCR検査', 'Unnamed: 10': '抗原検査'}, inplace=True)

    df['開始（予定）日'] = df['開始（予定）日'].apply(normalize_date)
    df['PCR検査'] = df['PCR検査'].apply(normalize_test_type)
    df['抗原検査'] = df['抗原検査'].apply(normalize_test_type)

    update_date = get_last_update_date()
    df.to_csv(f'../data/chiba/{update_date}.csv')


def get_latest_excel_url() -> str:
    """Get the latest Excel URL."""
    soup = get_soup()
    excel_link = soup.find(class_='icon_excel', text=re.compile('検査実施拠点一覧'))['href']
    return DOMAIN + excel_link


def get_last_update_date() -> date:
    """Get the latest updated date."""
    soup = get_soup()
    date_str = soup.select_one('#kensajisshitenpoichiran + span').text
    return normalize_date(date_str)


def get_soup():
    r = requests.get(WEBSITE_URL)
    r.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup


def normalize_date(d: datetime.datetime | str) -> date:
    """Normalize date strings mixed with Japanese and Western representation. Sometimes, they are ill-formatted.

    Example: '令和４年8月１1' -> '2022-08-11'
    """
    if type(d) is datetime.datetime:
        return d.date()

    if type(d) is str:
        d = unicodedata.normalize('NFKC', d)
        regex = re.compile(r'.*令和(?P<year>\d+)年(?P<month>\d+)月(?P<day>\d+)日?.*')
        m = regex.match(d)
        return datetime.date(year=int(m['year']) + 2018, month=int(m['month']), day=int(m['day']))

    raise ValueError('date is unexpected value')


def normalize_test_type(availablility: str) -> bool:
    """Convert '○' or null to a boolean value."""
    if availablility in ['○', '〇']:
        return True
    return False


if __name__ == '__main__':
    main()

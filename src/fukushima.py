# Fukushima: fetch the latest Excel data and save it as CSV file
from __future__ import annotations

import os
import re
from datetime import date

import bs4
import pandas as pd
import requests

from utils import normalize_date, normalize_test_type, convert_excel_date_number

DOMAIN = 'https://www.pref.fukushima.lg.jp'
WEBSITE_URL = f'{DOMAIN}/sec/01010a/tourokujigyousha.html'


def main():
    url = get_latest_excel_url()
    df = pd.read_excel(url, skiprows=1, index_col='№')[1:]
    df.index = df.index.astype(int)
    df.rename(columns={
        '検査方法': 'pcr',
        'Unnamed: 7': 'antigen',
        '実施方式': '対面',
        'Unnamed: 9': 'オンライン',
        'Unnamed: 10': 'ドライブスルー',
    }, inplace=True)
    df.columns = df.columns.map(lambda x: x.replace('\n', ''))
    print(df['事業開始日'])

    df['施設等名称'] = df['施設等名称'].apply(lambda x: x.replace('\n', ''))
    df['所在地'] = df['所在地'].apply(lambda x: f'福島県 {x}')
    df['pcr'] = df['pcr'].apply(normalize_test_type)
    df['antigen'] = df['antigen'].apply(normalize_test_type)
    df['対面'] = df['対面'].apply(normalize_test_type)
    df['オンライン'] = df['オンライン'].apply(normalize_test_type)
    df['ドライブスルー'] = df['ドライブスルー'].apply(normalize_test_type)
    df['事業開始日'] = df['事業開始日'].apply(convert_excel_date_number)

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/fukushima/{update_date}.csv')
    df.to_csv(save_path)


def get_latest_excel_url() -> str:
    """Get the latest Excel URL."""
    soup = get_soup()
    excel_link = soup.find('a', text=re.compile('実施事業者リスト.+Excel'))['href']
    return DOMAIN + excel_link


def get_last_update_date() -> date:
    """Get the latest updated date."""
    soup = get_soup()
    date_str = soup.find('p', text=re.compile('令和.+時点')).text
    return normalize_date(date_str)


def get_soup():
    r = requests.get(WEBSITE_URL)
    r.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(r.text, 'xml')
    return soup


if __name__ == '__main__':
    main()

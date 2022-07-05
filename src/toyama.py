# Miyagi: fetch the latest Excel data and save it as CSV file
from __future__ import annotations

import os
from datetime import date

import bs4
import pandas as pd
import requests

from utils import normalize_date, normalize_test_type

DOMAIN = 'https://toyama-muryokensa.jp/'
WEBSITE_URL = f'{DOMAIN}'


def main():
    url = get_latest_excel_url()
    df = pd.read_excel(url, skiprows=2, index_col='No')[1:]

    df.columns = df.columns.map(lambda x: x.replace('\n', ''))
    df.rename(columns={'実施可能な検査方法': 'pcr', 'Unnamed: 9': 'antigen'}, inplace=True)

    df['pcr'] = df['pcr'].apply(normalize_test_type)
    df['antigen'] = df['antigen'].apply(normalize_test_type)

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/toyama/{update_date}.csv')
    df.to_csv(save_path, index=False)


def get_latest_excel_url() -> str:
    """Get the latest Excel URL."""
    soup = get_soup()
    return [a for a in soup.find_all('a') if 'Excel' in a.text][0]['href']


def get_last_update_date() -> date:
    """Get the latest updated date."""
    excel_url = get_latest_excel_url()
    first_line = pd.read_excel(excel_url).iloc[0]
    return normalize_date(str(first_line))


def get_soup():
    r = requests.get(WEBSITE_URL)
    r.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup


if __name__ == '__main__':
    main()

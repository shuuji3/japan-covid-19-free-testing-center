# Miyagi: fetch the latest Excel data and save it as CSV file
from __future__ import annotations

import os
import re
from datetime import date

import bs4
import pandas as pd
import requests

from utils import normalize_date, normalize_test_type

DOMAIN = 'https://www.pref.miyagi.jp/'
WEBSITE_URL = f'{DOMAIN}/soshiki/kikisom/vtp/teityaku.html'


def main():
    url = get_latest_excel_url()
    df = pd.read_excel(url, skiprows=1)
    df.columns = df.columns.map(lambda x: x.replace('\n', ''))

    df['事業所名'] = df['事業所名'].apply(lambda x: x.replace('\n', ' '))
    df['事業所所在地'] = df['事業所所在地'].apply(lambda x: re.sub(r'〒\d{3}.\d{4}\s+', '', x.replace('\n', ' ')))
    df['事業開始日'] = df['事業開始日'].apply(normalize_date)
    df['PCR検査の実施'] = df['PCR検査の実施'].apply(normalize_test_type)
    df['抗原定性検査の実施'] = df['抗原定性検査の実施'].apply(normalize_test_type)

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/miyagi/{update_date}.csv')
    df.to_csv(save_path, index=False)


def get_latest_excel_url() -> str:
    """Get the latest Excel URL."""
    soup = get_soup()
    excel_link = soup.find(class_='icon_excel', text=re.compile('エクセルファイル'))['href']
    return DOMAIN + excel_link


def get_last_update_date() -> date:
    """Get the latest updated date."""
    soup = get_soup()
    date_str = next(h4.text for h4 in soup.select('h4') if '無料検査実施場所' in h4.text)
    return normalize_date(date_str)


def get_soup():
    r = requests.get(WEBSITE_URL)
    r.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    return soup


if __name__ == '__main__':
    main()

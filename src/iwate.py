# Iwate: fetch the latest HTML table from their website and save it as CSV file
from __future__ import annotations

import os
from datetime import date

import pandas as pd

from utils import normalize_date, normalize_test_type

WEBSITE_URL = 'https://www.pref.iwate.jp/kurashikankyou/iryou/seido/1048469/1048471.html'


def main():
    df = pd.read_html(WEBSITE_URL, index_col='番号')[0]

    # Surprisingly, they write note sentences inside a "name" cell!!
    # This extract only the first line to prevent note text from being included in a place name
    df['名称実施場所'] = df['名称実施場所'].apply(lambda name: name.split()[0])

    df['実施場所所在地'] = df['実施場所所在地'].map(lambda name: '岩手県 ' + name)
    df['事業開始日'] = df['事業開始日'].apply(normalize_date)
    df['PCR 等検査'] = df['PCR 等検査'].apply(normalize_test_type)
    df['抗原定性 検査'] = df['抗原定性 検査'].apply(normalize_test_type)

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/iwate/{update_date}.csv')
    df.to_csv(save_path)


def get_last_update_date() -> date:
    """Get the latest updated date."""
    return date.today()


if __name__ == '__main__':
    main()

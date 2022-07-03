# Tokyo: fetch the latest Excel data and save it as CSV file
from __future__ import annotations

import os
from datetime import date

import pandas as pd

from utils import normalize_date, normalize_test_type


def main():
    url = get_latest_excel_url()
    df = pd.read_csv(url, encoding='shift-jis', skiprows=1)

    df['PCR検査等'] = df['PCR検査等'].apply(normalize_test_type)
    df['抗原定性検査'] = df['抗原定性検査'].apply(normalize_test_type)

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/tokyo/{update_date}.csv')
    df.to_csv(save_path, index=None)


def get_latest_excel_url() -> str:
    """Get the latest Excel URL."""
    return 'https://tokyo-kensasuishin.jp/jigyousha/csv'


def get_last_update_date() -> date:
    """Get the latest updated date."""
    url = get_latest_excel_url()
    df = pd.read_csv(url, encoding='shift-jis')
    return normalize_date(str(df.iloc[0]))


if __name__ == '__main__':
    main()

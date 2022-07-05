# Kanagawa: Fetch kintone database records and save it as a CSV file
import datetime
import json
import os

import pandas as pd
import requests

from utils import normalize_test_type


def get_last_update_date() -> datetime.date:
    return datetime.date.today()


def main():
    records = fetch_all_records()
    places = map(convert_place, records)
    df = pd.DataFrame(places)
    df.set_index('id')

    update_date = get_last_update_date()
    dirname = os.path.dirname(__file__)
    save_path = os.path.join(dirname, f'../data/kanagawa/{update_date}.csv')
    df.to_csv(save_path, index=False)


def fetch_all_records():
    page = 1
    records = []

    # Prevent infinite loop. Over 10000 (400 * 25) records is too much.
    while page <= 25:
        url_base = (
            'https://3ce11065.viewer.kintoneapp.com/public/api/records/'
            'e7332448a3594bdd3487cfb6616126aa24ab906ed6f58158f8e30b38d0a436f1/'
            '{page}?num=400'
        )
        r = requests.get(url_base.format(page=page))
        data = json.loads(r.text)
        for record in data['records']:
            records.append(record)

        if len(records) >= data['totalCount']:
            break

        page += 1

    return records


def convert_place(record: dict) -> dict[str, str]:
    return {
        'id': record['$id']['value'],
        'name': record['文字列__1行__0']['value'].replace('\u3000', ' '),
        'address': record['文字列__1行__1']['value'].replace('\u3000', ' '),
        'pcr': normalize_test_type(record['ドロップダウン_1']['value']),
        'antigen': normalize_test_type(record['ドロップダウン_2']['value']),
    }


if __name__ == '__main__':
    main()

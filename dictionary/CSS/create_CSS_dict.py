import csv
from pydantic import BaseModel

import requests

api_id = 'AKfycbxDh6yskJki54aHWTLYwgjM55tzfAcZtSdD5IfA4l6Gjo43K6c7Hmd8-sUc35E9Hr_TZA'
end_point = f'https://script.google.com/macros/s/{api_id}/exec'


class Word(BaseModel):
    en: str
    tw: str
    type: str
    # parent: Word


def save(title: str, data_set: list):
    with open(f'{title}.csv', 'wt') as f:
        writer = csv.writer(f)
        writer.writerows(data_set)


if __name__ == '__main__':

    r = requests.get(end_point)

    data = [Word(**row) for row in r.json()]
    data = [[row.en, row.tw] for row in data if row.en != '']
    print(len(data))

    save('CSS', data)

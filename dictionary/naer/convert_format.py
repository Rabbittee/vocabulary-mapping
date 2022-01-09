import re
from os import listdir
from os.path import isfile, join


def get_file_paths(root: str) -> list:
    files = listdir(root)

    paths = []
    for f in files:
        fullpath = join(root, f)
        if isfile(fullpath):
            paths.append(fullpath)
    paths.sort()
    return paths


def get_raw_data(file_path: str) -> str:
    with open(file_path, 'rt') as fin:
        data = fin.read()
    return data


def clean_data(raw_data: str) -> list:
    data = []
    rows = re.findall(r'<tr>(.+?)</tr>', raw_data)

    for row in rows:
        items = re.findall(r'<td>(.+?)</td>', row.strip())
        data.append(list(map(lambda item: item.strip(), items)))

    return data


if __name__ == '__main__':
    paths = get_file_paths('./electronicComputer/Term_613')
    output = []
    for file_path in paths:
        raw_data = get_raw_data(file_path)
        output += clean_data(raw_data)

    print(f'total {len(output)}')
    print(output[:10])

import re
import os
import csv
from typing import List, Optional, Union

from pydantic import BaseModel
import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download("punkt")


class Heading(BaseModel):
    level: str
    content: str


class Page(BaseModel):
    title: str
    description: str
    headings: Optional[List[Heading]] = None
    # constent: List[str]


def read_file(file_path: str) -> str:
    with open(file_path, 'rt') as fin:
        text = fin.read()
    return text


def get_headings(text: str) -> List[Heading]:
    p = re.compile(
        r"(?P<level>#{1,3}) (<Heading ignore>)?(<Heading hidden>)?(?P<content>((?!</Heading>).)*)")
    return [Heading(**m.groupdict()) for m in p.finditer(text)]


def get_page_component(text: str):
    p = re.compile(
        r"title: (?P<title>.*)?\n(.*\n)?description: (?P<description>.*)")
    m = p.search(text)
    page = Page(**m.groupdict(), headings=get_headings(text))
    return page


def sum_segmentation(text: str, total: dict):
    tokens = nltk.tokenize.word_tokenize(text)
    for token in tokens:
        if token not in total:
            total[token] = 0
        total[token] += 1


def save(title: str, data_set: Union[dict, list]):
    if isinstance(data_set, dict):
        data_set = [[k, v] for k, v in sorted(
            data_set.items(), key=lambda item: item[1], reverse=True)]
    else:
        data_set = [
            [data[1:-1] if data.startswith(('"', "'")) else data] for data in data_set]

    with open(f'{title}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data_set)


if __name__ == '__main__':

    total_title = set()
    total_description = set()
    total_heading = set()

    doc_path = "../tailwindcss.com/src/pages/docs/"
    for file_name in os.listdir("../tailwindcss.com/src/pages/docs/"):
        if not file_name.endswith('.mdx'):
            continue

        file_path = os.path.join(doc_path, file_name)

        text = read_file(file_path)
        page = get_page_component(text)
        # print(page.title)
        # print(page.description)

        total_title.add(page.title)
        total_description.add(page.description)

        # sum_segmentation(page.title, total_title_description)
        # sum_segmentation(page.description, total_title_description)

        for heading in page.headings:
            total_heading.add(heading.content)
            # sum_segmentation(heading.content, total_heading)

    save('title', total_title)
    save('description', total_description)
    save('headings', total_heading)

    # for heading in page.headings:
    #     print(heading.content)

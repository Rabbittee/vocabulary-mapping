import re
import os
from typing import List, Optional
from pydantic import BaseModel


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
        r"(?P<level>#{1,3}) (<Heading ignore>)?(?P<content>((?!</Heading>).)*)")
    return [Heading(**m.groupdict()) for m in p.finditer(text)]


def get_page_component(text: str):
    p = re.compile(
        r"title: (?P<title>.*)?\n(.*\n)?description: (?P<description>.*)")
    m = p.search(text)
    page = Page(**m.groupdict(), headings=get_headings(text))

    if page.title.startswith(('"', "'")):
        page.title = page.title[1:-1]
    if page.description.startswith(('"', "'")):
        page.description = page.description[1:-1]
    return page


if __name__ == '__main__':

    doc_path = "../tailwindcss.com/src/pages/docs/"
    for file_name in os.listdir("../tailwindcss.com/src/pages/docs/"):
        if not file_name.endswith('.mdx'):
            continue

        file_path = os.path.join(doc_path, file_name)

        text = read_file(file_path)
        page = get_page_component(text)
        print(page.title)
        print(page.description)

        # for heading in page.headings:
        #     print(heading.content)

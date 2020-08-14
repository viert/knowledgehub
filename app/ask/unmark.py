import re
from typing import Set
from markdown import Markdown
from io import StringIO

USERNAME_RE = re.compile(r"(?:^|[^\\])@([.a-z0-9@_-]+)")
ESCAPE_SYMBOLS = "[*_"


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text.replace("\n", " "))
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail.replace("\n", " "))
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text: str) -> str:
    return __md.convert(text)


def extract_usernames(text: str) -> Set[str]:
    return set(USERNAME_RE.findall(text))


def escape(unmarked: str) -> str:
    for sym in ESCAPE_SYMBOLS:
        unmarked = unmarked.replace(sym, f"\\{sym}")
    return unmarked

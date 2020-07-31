import re
from typing import Optional
from .utils import cut

FIX_NON_LETTER = re.compile(r"[^\w\-_]")
FIX_SUFFIX = re.compile(r"[_\-]+$")

TRANSLITERATION_TABLE = {
    # RUSSIAN
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "_",
    "ы": "y",
    "ь": "_",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def transliterate_case_sensitive(text: str) -> str:
    translit = ""

    for sym in text:
        upper = sym.isupper()
        sym = sym.lower()
        res = TRANSLITERATION_TABLE[sym] if sym in TRANSLITERATION_TABLE else sym
        if upper:
            res = res.upper()
        translit += res
    return translit


def transliterate(text: str) -> str:
    translit = ""
    text = text.lower()
    for sym in text:
        if sym in TRANSLITERATION_TABLE:
            translit += TRANSLITERATION_TABLE[sym]
        else:
            translit += sym
    return translit


def hrid(text: str, max_len: Optional[int] = None) -> str:
    text = transliterate(text)
    text = FIX_NON_LETTER.sub("-", text)
    text = FIX_SUFFIX.sub("", text)
    if max_len is not None:
        text = cut(text, max_len)
    return text



def cut(text: str, max_len: int = 250) -> str:
    if len(text) <= max_len:
        return text
    i = max_len
    while i > 0:
        if text[i] == " ":
            text = text[:i].strip()
            return text + "..."
        i -= 1
    if i == 0:
        return text[:max_len] + "..."

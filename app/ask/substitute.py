import re
from glasskit import ctx


def substitute(text: str) -> str:
    substitutions = ctx.cfg.get("substitutions")
    if substitutions is None:
        return text

    for expr, sub in substitutions:
        try:
            expr = re.compile(expr)
        except re.error:
            ctx.log.debug("invalid substitution expression %s", expr)
            continue
        text = expr.sub(sub, text)

    return text

import re


def get_base_url(url: str) -> str:
    base_re = r"^.+?[^\/:](?=[?\/]|$)"
    return re.findall(base_re, url)[0]

from base64 import standard_b64encode
from os import path
from urllib.parse import quote

from bs4 import BeautifulSoup
from mako.template import Template


script_dir = path.abspath(path.dirname(__file__))


def _encode(s):
    return standard_b64encode(quote(s).encode("ascii")).decode("ascii")


def emit_stapidoc(content: str) -> str:
    soup = BeautifulSoup(content, "html5lib")
    link_literals = []
    links = soup.head.find_all("link")
    for ln in links:
        link_literals.append(str(ln))
        ln.decompose()

    template = Template(filename=path.join(script_dir, "stapidoc.mako"))
    return template.render(
        s_b64=_encode(soup.html.decode_contents()),
        ll_b64=[
            _encode(ln_literal) for ln_literal in link_literals
        ]
    )

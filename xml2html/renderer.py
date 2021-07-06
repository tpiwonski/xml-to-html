from __future__ import annotations

import typing

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("xml2html.movies"), autoescape=select_autoescape()
)


def render(data: typing.Any, template: str) -> str:
    return env.get_template(template).render(data=data)

from __future__ import annotations

import io
import typing

import requests


def load(url: str) -> typing.IO[bytes]:
    # response = requests.get(url, stream=True)
    # content = io.BytesIO()
    # for chunk in response.iter_content(chunk_size=1024):
    #     content.write(chunk)
    #
    # content.seek(0)
    # return content
    response = requests.get(url)
    return io.BytesIO(response.content)

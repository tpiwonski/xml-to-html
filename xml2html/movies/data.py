from __future__ import annotations

import typing
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Synopsis:
    text: str


@dataclass
class Rating:
    value: int


@dataclass
class Movie:
    title: str
    synopsis: Synopsis
    rating: Rating
    running_time: timedelta


@dataclass
class MovieList:
    movies: typing.List[Movie]

from __future__ import annotations

import typing
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import timedelta

from xml2html.movies.data import Movie, MovieList, Rating, Synopsis
from xml2html.parser import ElementParser
import regex


@dataclass
class SynopsisParser(ElementParser):
    tag = "synopsis"

    def end(self, e: ET.Element) -> typing.Any:
        text = " ".join([p.strip() for p in e.itertext() if p.strip()])
        return Synopsis(text=text)


@dataclass
class RatingParser(ElementParser):
    tag = "rating"

    def end(self, e: ET.Element) -> typing.Any:
        return Rating(value=(e.text.count("*") if e.text else 0))


@dataclass
class RunningTimeParser(ElementParser):
    tag = "running-time"

    def end(self, e: ET.Element) -> typing.Any:
        if e.text:
            m = regex.match("(?P<running_time>[0-9]+)", e.text.strip())
            if m:
                return timedelta(minutes=int(m["running_time"]))

        return timedelta(0)


@dataclass
class MovieParser(ElementParser):
    tag = "movie"
    children = [SynopsisParser, RatingParser, RunningTimeParser]

    def end(self, e: ET.Element) -> typing.Any:
        title_elem = e.find("heading/title")
        title = title_elem.text if title_elem is not None and title_elem.text else ""

        # rating_elem = e.find("heading/rating")
        # if rating_elem is not None and rating_elem.text:
        #     rating = Rating(value=rating_elem.text.count("*"))
        # else:
        #     rating = Rating(value=0)

        # return Movie(synopsis=self.data[0][1], rating=rating, title=title)

        e.clear()

        data = {t: d for t, d in self.data}
        return Movie(synopsis=data["synopsis"], rating=data["rating"], title=title, running_time=data["running-time"])


@dataclass
class MoviesListParser(ElementParser):
    tag = "movie-list"
    children = [MovieParser]

    def end(self, e: ET.Element) -> typing.Any:
        return MovieList(movies=[m[1] for m in self.data])

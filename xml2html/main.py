from xml2html.loader import load
from xml2html.movies.parsers import MoviesListParser
from xml2html.parser import parse
from xml2html.renderer import render

if __name__ == "__main__":
    html = render(
        parse(load("http://localhost:8000/movies.xml"), MoviesListParser), "main.html"
    )
    print(html)

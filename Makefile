lint:
	mypy xml2html && isort xml2html && black xml2html
server:
	python -m http.server

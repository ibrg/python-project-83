dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app

install:
	poetry install

lint: 
	python -m flake8 page_analyzer


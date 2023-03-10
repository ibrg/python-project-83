dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b http://0.0.0.0:8000 page_analyzer:app

install:
	poetry install

lint: 
	python -m flake8 page_analyzer

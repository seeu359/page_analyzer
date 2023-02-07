dev:
	poetry run flask --app page_analyzer:app run --reload

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

sort:
	poetry run isort .

lint:
	poetry run flake8

install:
	poetry install


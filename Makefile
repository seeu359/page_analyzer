dev:
	poetry run flask --app page_analyzer:app run --reload

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

sort:
	poetry run isort .

lint:
	poetry run flake8

p_install:
	poetry install

install:
	pip install -r requirements.txt

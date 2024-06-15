start:
	poetry run python main.py

black:
	poetry run black .

build:
	docker compose up --build
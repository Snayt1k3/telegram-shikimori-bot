start:
	alembic & poetry run python main.py

make alembic:
	poetry run alembic upgrade head

black:
	poetry run black src/

make start-celery:
	poetry run celery -A src.adapters.celery worker --loglevel=info
start:
	alembic & poetry run python main.py

make alembic:
	poetry run alembic upgrade head

black:
	poetry run black src/

start-celery:
	poetry run celery -A src.adapters.celery worker --loglevel=info

start-celery-beat:
	poetry run celery -A src.adapters.celery beat --loglevel=info
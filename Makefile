run:
	docker compose up --build

stop:
	docker compose down

lint:
	poetry run black  api-gateway/ telegram-bot/ --exclude "migrations/"
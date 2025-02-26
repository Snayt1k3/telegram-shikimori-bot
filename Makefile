run:
	docker compose up --build

stop:
	docker compose down

lint:
	poetry run black anime-service/ api-gateway/ auth-service/ telegram-bot/ --exclude "migrations/"
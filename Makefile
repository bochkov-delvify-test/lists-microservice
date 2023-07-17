.PHONY setup-mac:
setup-mac:
	brew install pyenv && pyenv install 3.11 && \
	brew install poetry && poetry self add poetry-dotenv-plugin && \
	poetry env use 3.11 && poetry install --with lint,test

do-lint:
	echo "Running Isort" && python -m isort delvify && \
	echo "Running Black" && python -m black delvify && \
	echo "Running Flake8" && python -m flake8 delvify && \
	echo "Running MyPy" && python -m mypy delvify

.PHONY lint:
lint:
	poetry run $(MAKE) do-lint

.PHONY test:
test:
	poetry run pytest

.PHONY test:
test-docker:
	docker build --target test -t delvify-test -f Dockerfile .
	docker run --env-file .env --rm delvify-test

.PHONY run:
run:
	docker-compose up --build --detach && \
	echo "Open http://localhost:8000/docs in your browser"

.PHONY stop:
stop:
	docker-compose stop

.PHONY clean:
clean: stop
	docker-compose down -v --rmi all

.PHONY: gen-migrations
gen-migrations: run migrate
	@read -p "Enter Alembic migration message: " message; \
	docker-compose exec api alembic revision --autogenerate -m "$$message" && \
	docker compose cp api:/home/app/migrations/versions/. ./migrations/versions/.

.PHONY: migrate
migrate:
	docker-compose exec api alembic upgrade head

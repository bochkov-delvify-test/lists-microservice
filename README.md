# lists-microservice

![checks status](https://github.com/delvify-assessment/lists-microservice/actions/workflows/pr.yml/badge.svg)

## Description

A microservice for managing lists of tasks based on FastAPI and Docker.

## Requirements

- [ ] Python 3.11+
- [ ] Poetry
- [ ] Make
- [ ] Docker with BuildKit support (24+ version)

## Installation

### For Mac users

* Install [Homebrew](https://brew.sh/)
* `make setup-mac`

### For other users

Please, refer to the [Makefile](Makefile) for the list of commands to run (check `setup-mac` target).  
Please, adjust them accordingly for your OS of choice.

## Development

### Lifecycle commands

Run the service as a Docker stack

```bash
make run 
```

If you are running the service for the first time, apply migrations by running:

```bash
make migrate
```

Run tests

```bash
make test
```

Run linters

```bash
make lint
```

To check the logs, run:

```bash
docker-compose logs
```

Or, for a specific service:

```bash
docker-compose logs api
```

Or use the Docker UI.

#### Dependency Management

Dependencies are managed by [Poetry](https://python-poetry.org/).     
To add a new dependency, run `poetry add <package-name>`.  
To start a new shell with the dependencies installed, run `poetry shell`.  
For a comfortable dev process, ensure you are installing the optional dependency groups by running

```bash
poetry install --with lint,test
```

#### Migrations

Migrations are managed by [Alembic](https://alembic.sqlalchemy.org/en/latest/).
After making changes to the models, run `make gen-migrations` to generate a new migration.
Then, run `make migrate` to apply a migration.  
Our migrations are not automatic by a concious decision.

#### API documentation

After the service is up and running, you can access the API documentation at:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

#### Code formatting

Please check the [Makefile](Makefile) for the authorities on a code style (check `do-lint` target).  
You can also use the [pre-commit](https://pre-commit.com/) tool to automatically format your code before committing.

#### CI/CD

The service is configured to run CI/CD on GitHub Actions.
The pipeline runs the following steps:

* Linting (every [push](.github/workflows/pr.yml))
* Testing (every [push](.github/workflows/pr.yml))
* Building and Pushing a Docker image to DockerHub (every [push to main](.github/workflows/deploy.yml))

## Project structure

```
├── .github - GitHub Actions configuration (linting, testing, building and pushing Docker image)
├── migrations - Alembic migrations
├── tests - Tests
├── delvify - Service code
│   ├── api - API endpoints
│   ├── core - Core service code
│   │   ├── db - Database configuration
│   │   ├── di - Dependency injection
│   │   ├── helpers - Helper functions
│   │   ├── logger - Logging configuration
│   │   ├── security - Creating JWT tokens
│   │   ├── settings - Service settings
│   │   ├── retries - Exponential backoff retries
│   ├── jobs - Scheduled jobs service
│   ├── crud - Database CRUD operations
│   ├── models - Database configuration
│   ├── schemas - Pydantic schemas
│   ├── services - Separated services
│   │   ├── notification - Notifications service
│   ├── main.py - Entrypoint

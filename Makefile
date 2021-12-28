.ONESHELL:

py := poetry run
python := $(py) python

package_dir := app
tests_dir := tests

code_dir := $(package_dir) $(tests_dir)


.PHONY: reformat
reformat:
	$(py) black $(code_dir)
	$(py) isort $(code_dir) --profile black --filter-files

.PHONY: dev-docker
dev-docker:
	docker compose -f=./deployment/docker-compose-dev.yml --env-file=./deployment/.env.dev up


.PHONY: dev-api
dev-api:
	$(py) uvicorn app.api.main:api --reload --env-file ./deployment/.env.dev

.PHONY: dev-bot
dev-bot:
	powershell ./deployment/tgbot.bat

.PHONY: prod
prod:
	docker compose -f=./deployment/docker-compose.yml --env-file=./deployment/.env.dev up

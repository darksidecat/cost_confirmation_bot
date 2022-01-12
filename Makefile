.ONESHELL:

py := poetry run
python := $(py) python

package_dir := app
tests_dir := tests

code_dir := $(package_dir) $(tests_dir)


define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	$(py) black $(code_dir)
	$(py) isort $(code_dir) --profile black --filter-files

.PHONY: dev-docker
dev-docker:
	docker compose -f=./deployment/docker-compose-dev.yml --env-file=./deployment/.env.dev up

.PHONY: dev-alembic
dev-alembic:
	$(call setup_env, ./deployment/.env.dev)
	alembic -c ./deployment/alembic.ini  upgrade head

.PHONY: dev-api
dev-api:
	$(py) uvicorn app.api.main:api --reload --env-file ./deployment/.env.dev

.PHONY: dev-bot
dev-bot:
	$(call setup_env, ./deployment/.env.dev)
	python -m app.tgbot --init_admin_db

.PHONY: prod
prod:
	docker compose -f=./deployment/docker-compose.yml --env-file=./deployment/.env.dev up

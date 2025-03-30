# Enable parallel execution
# 3 is the max parallel processes needed so far (for prestart)
MAKEFLAGS += -j3

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up

.PHONY: bash
bash:
	docker exec -it open-parlement bash

.PHONY: start
start:
	uvicorn open_parlement.asgi:application --workers 1 --host 0.0.0.0

.PHONY: locales
locales:
	python manage.py makemessages --all

.PHONY: static
static:
	python manage.py collectstatic --no-input --skip-checks

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate --no-input --skip-checks

.PHONY: format
format:
	isort .
	black .

.PHONY: lint
lint:
	flake8 .
	bandit -c pyproject.toml -r apps/ open_parlement/

.PHONY: test
test:
	coverage run
	coverage report

.PHONY: format-check
format-check:
	isort . -c
	black --check .

.PHONY: migrations-check
migrations-check:
	python manage.py makemigrations --noinput --check

TEMP_TRANSLATION_FILES := $(shell mktemp -d --suffix -projects-back-makemessages)
.PHONY: locales-check
locales-check:
# Copy translation files to a temp directory
	mkdir -p ${TEMP_TRANSLATION_FILES}/current ${TEMP_TRANSLATION_FILES}/new
	for trans_file in $(shell find locale/ -name '*.po'); do cp -r "$$trans_file" ${TEMP_TRANSLATION_FILES}/current/${trans_file}; done
# Create translation files
	python manage.py makemessages --all
	for trans_file in $(shell find locale/ -name '*.po'); do cp -r "$$trans_file" ${TEMP_TRANSLATION_FILES}/new/${trans_file}; done
# Compare generated translation files with the originals
	diff -r -I "POT-Creation-Date: .*" ${TEMP_TRANSLATION_FILES}/current ${TEMP_TRANSLATION_FILES}/new
# Cleanup
	rm -rf ${TEMP_TRANSLATION_FILES}

# Makefile for Django project

PYTHON=python
MANAGE=manage.py

run:
	$(PYTHON) $(MANAGE) runserver 0.0.0.0:8000

setup-db:
	$(PYTHON) $(MANAGE) makemigrations
	$(PYTHON) $(MANAGE) migrate

run-pre-commit:
	uv run pre-commit run --all-files

run-ruff:
	ruff check . && \
	ruff format . && \
	wait

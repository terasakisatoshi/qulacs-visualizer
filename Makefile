PYTEST := poetry run pytest -v
PYSEN := poetry run pysen

.PHONY: all
all: format lint test

.PHONY: test
test:
	$(PYTEST)

.PHONY: test-with-latex
test-with-latex:
	$(PYTEST) --runlatex

.PHONY: lint
lint:
	$(PYSEN) run lint

.PHONY: format
format:
	$(PYSEN) run format

.PHONY: check
check: format lint

.DEFAULT_GOAL := all
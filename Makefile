.PHONY=format
format:
	@poetry run black .
	@poetry run isort .

.PHONY=lint
lint:
	@poetry run isort --check .
	@poetry run black --check .
	@poetry run pflake8 tests src features

.PHONY=unit-tests
unit-tests:
	@poetry run python -m pytest

.PHONY=acceptance-tests
acceptance-tests:
	@poetry run behave

.PHONY=test
test: lint unit-tests acceptance-tests

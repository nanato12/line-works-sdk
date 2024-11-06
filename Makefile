.PHONY: init
init:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	test -f .env || cp .env.template .env

.PHONY: run
run:
	python main.py

.PHONY: lint
lint:
	ruff --version
	ruff check
	ruff format --check
	mypy .

.PHONY: fmt
fmt:
	ruff --version
	ruff format
	ruff check --fix

.PHONY: build
build:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: test-pypi
test-pypi:
	twine upload --repository pypitest dist/* --verbose

.PHONY: pypi
pypi:
	twine upload --repository pypi dist/* --verbose

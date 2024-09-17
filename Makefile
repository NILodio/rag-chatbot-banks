MYPY_DIRS := $(shell find components bin ! -path '*.egg-info*' ! -path '*__pycache__*' -type d -maxdepth 0 -mindepth 0 | xargs)
COV_DIRS := $(shell find components layer/shared bin assets ! -path '*.egg-info*' ! -path '*__pycache__*' -type d -maxdepth 2 -mindepth 0 | xargs)
ARTIFACTS_DIR ?= build


.PHONY: test
test: copy_assets_to_shared
	pytest -rs

.PHONY: mypy_package
mypy_package:
	python -m mypy -p shared

.PHONY: mypy
mypy: mypy_package $(MYPY_DIRS)
	python -m mypy $(foreach d, $(MYPY_DIRS),$(d)) --explicit-package-bases

.PHONY: pre-commit-routine
pre-commit-routine: format mypy unit_tests

.PHONY: format
format:
	python -m isort .
	python -m black .
	python -m ruff check . --fix

.PHONY: install
install:
	python -m pip install --upgrade pip aws-sam-cli
	python -m pip install --editable .
	python -m pip install -U -r requirements/requirements.dev.txt --index-url https://elasticpypi:lMExlbachG9cYswBVxE1ZyieW7VMjdgxPJGBvbJtnjvsloMK@4erpxjkulc.execute-api.us-east-1.amazonaws.com/prod/simple/ --extra-index-url https://pypi.org/simple/

.PHONY: develop
develop: install
	python -m pre_commit install

.PHONY: export_dev_env
export_dev_env:
    export $(cat .env.dev | xargs)


.PHONY: build
build:
	rm -rf dist || true
	python -m build -w

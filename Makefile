# These have been configured to only really run short tasks. Longer form tasks
# are usually completed in github actions.

NAME := Sim2Real_py3
PACKAGE_NAME := Sim2Real_py3

DIR := "${CURDIR}"
SOURCE_DIR := ${PACKAGE_NAME}
TESTS_DIR := tests
SCRIPTS_DIR := scripts

.PHONY: help install-dev check format clean test

help:
	@echo "Makefile ${NAME}"
	@echo "* install-dev      to install all dev requirements and install pre-commit"
	@echo "* clean            to clean any doc or build files"
	@echo "* check            to check the source code for issues"
	@echo "* format           to format the code with black and isort"
	@echo "* test             to run the tests"

PYTHON ?= python
PYTEST ?= python -m pytest
PIP ?= python -m pip
MAKE ?= make
BLACK ?= black
ISORT ?= isort
PYDOCSTYLE ?= pydocstyle
FLAKE8 ?= flake8

install-dev:
	$(PIP) install -e ".[dev]"

check-black:
	$(BLACK) ${SOURCE_DIR} --check || :
	$(BLACK) ${TESTS_DIR} --check || :
	$(BLACK) ${SCRIPTS_DIR} --check || :

check-isort:
	$(ISORT) ${SOURCE_DIR} --check || :
	$(ISORT) ${TESTS_DIR} --check || :
	$(ISORT) ${SCRIPTS_DIR} --check || :

check-pydocstyle:
	$(PYDOCSTYLE) ${SOURCE_DIR} || :

check-flake8:
	$(FLAKE8) ${SOURCE_DIR} || :
	$(FLAKE8) ${TESTS_DIR} || :
	$(FLAKE8) ${SCRIPTS_DIR} || :

check: check-black check-isort check-flake8 check-pydocstyle

format-black:
	$(BLACK) ${SOURCE_DIR}
	$(BLACK) ${TESTS_DIR}
	$(BLACK) ${SCRIPTS_DIR}

format-isort:
	$(ISORT) ${SOURCE_DIR}
	$(ISORT) ${TESTS_DIR}
	$(ISORT) ${SCRIPTS_DIR}

format: format-black format-isort

test:
	$(PYTEST) ${TESTS_DIR}

# Clean up any builds in ./dist as well as doc, if present
clean: 
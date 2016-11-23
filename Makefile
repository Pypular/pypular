.PHONY: clean-pyc clean

help:
	@echo "clean - remove Python file artifacts"
	@echo "lint - check style with flake8"

clean: clean-pyc

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint:
	flake8 .

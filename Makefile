DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_TEST=docker-compose -f docker-compose_testing.yml

.PHONY: clean-pyc clean

help:
	@echo "clean - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "run_app - run app using docker"

clean: clean-pyc

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint:
	flake8 .

run_app:
	$(DOCKER_COMPOSE) build app
	$(DOCKER_COMPOSE) up app


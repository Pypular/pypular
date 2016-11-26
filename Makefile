DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_TEST=docker-compose -f docker-compose_testing.yml

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

run_test:
	$(DOCKER_COMPOSE_TEST) rm -f test_redis test_postgres
	$(DOCKER_COMPOSE_TEST) build
	$(DOCKER_COMPOSE_TEST) run --rm -e DJANGO_SETTINGS_MODULE=code_challenge.settings test python manage.py test --nomigrations

run_app:
	$(DOCKER_COMPOSE) build app
	$(DOCKER_COMPOSE) up app


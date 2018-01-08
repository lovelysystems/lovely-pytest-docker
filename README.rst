====================
Lovely Pytest Docker
====================

Create simple Pytest_ fixtures for writing integration tests based on Docker
containers. The framework provides a service class to start and stop containers
based Docker Compose. Each single container can be started individually.

Some parts of this package are taken from
https://github.com/AndreLouisCaron/pytest-docker


Usage with Pytest
=================

The docker compose file should contain all desired containers and the ports
should be exposed. In the following example we want to start the app to test
and a SQL database (Crate). Let's assume there is a ``Dockerfile`` for the app
in the same folder as the docker compose file::

    version: "3"
    services:
      app:
        build: .
        ports:
          - "8080"
        depends_on:
          - "crate"

      crate:
        image: crate:latest
        ports:
          - "4200"

In the ``conftest.py`` file we can declare the docker fixtures for each service
we want to be able to start in the tests::

    import pytest

    @pytest.fixture(scope='session')
    def docker_app(docker_services):
        docker_services.start('app')
        public_port = docker_services.wait_for_service("app", 8080)
        url = "http://{docker_services.docker_ip}:{public_port}".format(**locals())
        return url

    @pytest.fixture(scope='session')
    def docker_crate(docker_services):
        docker_services.start('crate')
        public_port = docker_services.wait_for_service("crate", 4200)
        dsn = "{docker_services.docker_ip}:{public_port}".format(**locals())
        return dsn

In many cases you will want to override the location for the docker compose
files. Just overwrite the ``docker_compose_files`` fixture in your
``conftest.py`` file::

    @pytest.fixture(scope='session')
    def docker_compose_files(pytestconfig):
        """Get the docker-compose.yml absolute path.
        Override this fixture in your tests if you need a custom location.
        """
        return [
            project_path('docker', 'docker-compose.yml'),
        ]

In your test file declare the fixtures you want to use::

    def test_something(docker_app, docker_crate):
        # e.g. initialize database
        ...
        # test something (e.g. request to docker_app)
        ...

A working configuration and test example can be found in the ``tests`` folder
of this package.


Run Tests
=========

Tests are held in the ``tests`` directory. Running tests is done via the
pytest package with::

    ./gradlew pytest


.. _Pytest: http://doc.pytest.org

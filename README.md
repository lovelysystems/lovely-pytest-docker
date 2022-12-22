# Lovely Pytest Docker

[![PyPI](https://img.shields.io/pypi/v/lovely-pytest-docker)](https://pypi.org/project/lovely-pytest-docker/)
[![PyPI](https://img.shields.io/pypi/pyversions/lovely-pytest-docker)](https://pypi.org/project/lovely-pytest-docker/)
[![Build Status](https://app.travis-ci.com/lovelysystems/lovely-pytest-docker.svg?branch=master)](https://app.travis-ci.com/lovelysystems/lovely-pytest-docker)

Create simple Pytest_ fixtures for writing integration tests based on Docker
containers. The framework provides a service class to start and stop containers
based Docker Compose. Each single container can be started individually.

Some parts of this package are taken from
https://github.com/AndreLouisCaron/pytest-docker

## Usage with Pytest

The docker compose file should contain all desired containers and the ports
should be exposed. In the following example we want to start the app to test
and a SQL database (Crate). Let's assume there is a ``Dockerfile`` for the app
in the same folder as the docker compose file.

```yaml


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
```

In the ``conftest.py`` file we can declare the docker fixtures for each service
we want to be able to start in the tests.

```python

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
```

By default the fixture will look for the ``docker-compose.yml`` file in the
``tests`` subfolder of the path where ``pytest.ini`` resides (or the project's
root directory if no ini file is given - as in the tests example). In many
cases you will want to override the location for the docker compose files. Just
overwrite the ``docker_compose_files`` fixture in your ``conftest.py`` file.

```python
    @pytest.fixture(scope='session')
    def docker_compose_files(pytestconfig):
        """Get the docker-compose.yml absolute path.
        Override this fixture in your tests if you need a custom location.
        """
        return [
            project_path('docker', 'docker-compose.yml'),
        ]
```

In your test file declare the fixtures you want to use:

```python
    def test_something(docker_app, docker_crate):
        # e.g. initialize database
        ...
        # test something (e.g. request to docker_app)
        ...
```

A working configuration and test example can be found in the ``tests`` folder
of this package.

## Execution in Docker Container

It's possible to execute a command inside one of the Docker containers. Use
the ``exec`` method of the ``docker_services`` fixture::

```python
    def test_execute(docker_services):
        # the first argument is the service name of the compose file,
        # the following arguments build the command to run
        res = docker_services.execute('crate', 'ls', '-a')
```

## Stopping a Docker Container

It's possible to stop single Docker containers. Use
the ``stop`` method of the ``docker_services`` fixture::

    def test_stop(docker_services):
        # the first argument is the service name of the compose file,
        # the following arguments build the command to run
        res = docker_services.stop('crate')

## Wait for Service

The ``wait_for_service`` method of the service module checks whether the
docker service is really started. By default it makes a HTTP GET request to the
server's ``/`` endpoint. The service will retry to check until a timeout of
30 seconds has passed.

### Custom Service Checker

Some services may work differently and require a custom checker.

Create a custom service checker function which receives the IP address and the
port as parameters::

```python
    def custom_service_checker(ip_address, port):
        # if service is ready
        return True
        # otherwise return False
```

In the fixture provide the custom service checker function as ``check_service``
parameter to the ``wait_for_service`` method::

```python
    @pytest.fixture(scope='session')
    def docker_custom_service(docker_services):
        docker_services.start('custom_service')
        public_port = docker_services.wait_for_service(
            "app",
            8080,
            check_server=custom_service_checker
        )
        url = "http://{docker_services.docker_ip}:{public_port}".format(**locals())
        return url
```

To use another request path with the default checker the `url_checker` method
can be used to create a `check_url` method for another path::

```python
    docker_services.wait_for_service(
        "app",
        8080,
        check_server=url_checker('/probe_status'),
    )
```

## Run Tests

Tests are held in the ``tests`` directory. Running tests is done via the
pytest package with::

```shell
    ./gradlew pytest
```

.. _Pytest: http://doc.pytest.org

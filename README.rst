====================
Lovely Pytest Docker
====================

.. image:: https://img.shields.io/pypi/v/lovely-pytest-docker.svg
    :target: https://pypi.org/project/lovely-pytest-docker/

.. image:: https://img.shields.io/pypi/pyversions/lovely-pytest-docker.svg
    :target: https://pypi.org/project/lovely-pytest-docker/

.. image:: https://travis-ci.com/lovelysystems/lovely-pytest-docker.svg?branch=master
    :target: https://travis-ci.com/lovelysystems/lovely-pytest-docker


Create simple Pytest_ fixtures for writing integration tests based on Docker
containers. The framework provides a service class to start and stop containers
based Docker Compose. Each single container can be started individually.

Some parts of this package are taken from
https://github.com/AndreLouisCaron/pytest-docker


Usage with Pytest
=================

A working configuration and test example can be found in the ``tests`` folder
of this package.

By default the fixture will look for the ``docker-compose.yml`` file in the
``tests`` subfolder of the path where ``pytest.ini`` resides (or the project's
root directory if no ini file is given - as in the tests example). In many
cases you will want to override the location for the docker compose files. Just
overwrite the ``docker_compose_files`` fixture in your ``conftest.py`` file::

    @pytest.fixture(scope='session')
    def docker_compose_files(pytestconfig):
        """Get the docker-compose.yml absolute path.
        Override this fixture in your tests if you need a custom location.
        """
        return [
            project_path('docker', 'docker-compose.yml'),
        ]


Execution in Docker Container
=============================

It's possible to execute a command inside one of the Docker containers. Use
the ``exec`` method of the ``docker_services`` fixture::

    def test_exec(docker_services):
        # the first argument is the service name of the compose file,
        # the following arguments build the command to run
        res = docker_services.exec('crate', 'ls', '-a')


Wait for Service
================

The ``wait_for_service`` method of the service module checks whether the
docker service is really started. By default it makes a HTTP GET request to the
server's ``/`` endpoint. The service will retry to check until a timeout of
30 seconds has passed.

Custom Service Checker
----------------------

Some services may work differently and require a custom checker.

Create a custom service checker function which receives the IP address and the
port as parameters::

    def custom_service_checker(ip_address, port):
        # if service is ready
        return True
        # otherwise return False

In the fixture provide the custom service checker function as ``check_service``
parameter to the ``wait_for_service`` method::

    @pytest.fixture(scope='session')
    def docker_custom_service(docker_services):
        docker_services.start('custom_service')
        public_port = docker_services.wait_for_service(
            "app",
            8080,
            check_service=custom_service_checker
        )
        url = "http://{docker_services.docker_ip}:{public_port}".format(**locals())
        return url


Run Tests
=========

Tests are held in the ``tests`` directory. Running tests is done via the
pytest package with::

    ./gradlew pytest


.. _Pytest: http://doc.pytest.org

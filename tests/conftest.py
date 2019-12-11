import pytest

from testing import project_path


@pytest.fixture(scope='session')
def docker_hello_world(docker_services):
    """Fixture for the specific Hello World container.

    Depends on the `docker_services` fixture and returns the public url for the
    docker container's service.
    """
    docker_services.start('hello')
    public_port = docker_services.wait_for_service("hello", 80)
    url = "http://{docker_services.docker_ip}:{public_port}".format(**locals())
    return url


@pytest.fixture(scope='session')
def docker_hello_world2(docker_services):
    """Fixture for the second Hello World container.

    Depends on the `docker_services` fixture and returns the public url for the
    docker container's service.
    """
    docker_services.start('hello2')
    public_port = docker_services.wait_for_service("hello2", 80)
    url = "http://{docker_services.docker_ip}:{public_port}".format(**locals())
    return url


@pytest.fixture(scope='session')
def docker_services_project_name():
    return "lovely-pytest-docker"


@pytest.fixture(scope='session')
def docker_compose_command():
    """The path to the docker-compose command, which defaults to `docker-compose`.
    In this example we use the docker-compose command installed by the projects dev dependencies by
    providing the absolute path to the executable.
    """
    return project_path("v", "bin", "docker-compose")

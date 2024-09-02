from six.moves.urllib.request import urlopen
import time


def test_hello_world(docker_hello_world):
    """Test if the container is reachable.

    The docker_hello_world fixture is used, so the container will start on test
    startup. Do a request to the docker service and read the body.
    """
    res = urlopen(docker_hello_world).read()
    assert b'<title>The Hello world page</title>' in res


def test_single_container(docker_hello_world, docker_services):
    """Test if only the requested containers are started.

    The container for hello2 is never started as the fixture is not used.s
    """
    res = docker_services._docker_compose.execute("ps")
    assert 'hello' in res
    assert 'hello2' not in res


def test_stop_single_container(docker_hello_world, docker_hello_world2, docker_services):
    """Test if only the requested containers are stope.

    The container for hello2 is started by the fixture and stopped via function.
    """
    res = docker_services._docker_compose.execute("ps")
    assert 'hello'  in res
    assert 'hello2' in res
    docker_services.stop("hello2")
    res = docker_services._docker_compose.execute('ps', '--services', '--filter', 'status=running')
    assert 'hello2' not in res
    docker_services.start("hello2")
    res = docker_services._docker_compose.execute('ps', '--services', '--filter', 'status=running')
    assert 'hello2' in res


def test_execute(docker_services):
    """Test the exec method.

    The exec method executes a command inside a docker command.
    """
    res = docker_services.execute('hello', 'ls', '-a')
    assert res.startswith('.\n..\n.dockerenv\n')


# counter
custom_checker_called = 0


def custom_checker(ip_address, port):
    global custom_checker_called
    if custom_checker_called > 1:
        return True
    custom_checker_called += 1
    return False


def test_custom_checker(docker_services):
    """Test a custom checker in the wait_for_service method."""

    docker_services.wait_for_service("hello", 8080, check_server=custom_checker)
    assert custom_checker_called > 1


def test_custom_docker_service_project_name(docker_hello_world, docker_services):
    """Test a custom project name for docker services.

    Project name can be defined as fixture in conftest.py
    """
    res = docker_services._docker_compose.execute("ps")
    assert 'lovely-pytest-docker' in res

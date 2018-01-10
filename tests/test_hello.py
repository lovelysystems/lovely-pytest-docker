from urllib.request import urlopen


def test_hello_world(docker_hello_world):
    """Test if the container is reachable.

    The docker_hello_world fixture is used, so the container will start on test
    startup. Do a request to the docker service and read the body.
    """
    res = urlopen(docker_hello_world).read()
    assert b'<title>HTTP Hello World</title>' in res


def test_single_container(docker_hello_world, docker_services):
    """Test if only the requested containers are started.

    The container for hello2 is never started as the fixture is not used.s
    """
    res = docker_services._docker_compose.execute("ps")
    assert 'hello' in res
    assert 'hello2' not in res


def test_exec(docker_services):
    """Test the exec method.

    The exec method executes a command inside a docker command.
    """
    res = docker_services.exec('hello', 'ls', '-a')
    assert res == '.\n..\nindex.html\n'


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

    docker_services.wait_for_service("hello", 80, check_server=custom_checker)
    assert custom_checker_called > 1

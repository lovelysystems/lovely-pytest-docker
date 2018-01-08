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

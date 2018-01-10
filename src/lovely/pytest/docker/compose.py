import os
import pytest
import re
import subprocess
import time
import timeit

from urllib.request import urlopen
from urllib.error import URLError


def check_url(docker_ip, public_port):
    """Check if a service is reachable.

    Makes a simple GET request to '/' of the HTTP endpoint. Service is
    available if returned status code is < 500.
    """
    url = 'http://{}:{}'.format(docker_ip, public_port)
    try:
        r = urlopen(url)
        return r.status < 500
    except URLError as e:
        # If service returns e.g. a 404 it's ok
        return e.code < 500
    except Exception as e:
        # Possible service not yet started
        return False


def execute(command, success_codes=(0,)):
    """Run a shell command."""
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=False,
        )
        status = 0
    except subprocess.CalledProcessError as error:
        output = error.output or b''
        status = error.returncode
        command = error.cmd
    output = output.decode('utf-8')
    if status not in success_codes:
        raise Exception(
            'Command %r returned %d: """%s""".' % (command, status, output)
        )
    return output


class Services(object):
    """A class which encapsulates services from docker compose definition.

    This code is partly taken from
    https://github.com/AndreLouisCaron/pytest-docker
    """

    def __init__(self, compose_files, project_name='pytest'):
        self._docker_compose = DockerComposeExecutor(
            compose_files, project_name
        )
        self._services = {}
        self.docker_ip = docker_ip()

    def start(self, *services):
        """Ensures that the given services are started via docker compose.

        :param services: the names of the services as defined in compose file
        """
        self._docker_compose.execute('up', '--build', '-d', *services)

    def exec(self, service, *cmd):
        """Execute a command inside a docker container.

        :param service: the name of the service as defined in compose file
        :param cmd: list of command parts to execute
        """
        return self._docker_compose.execute('exec', '-T', service, *cmd)

    def wait_for_service(self, service, private_port, check_server=check_url):
        """
        Waits for the given service to response to a http GET.

        :param service: the service name as defined in the docker compose file
        :param private_port: the private port as defined in docker compose file
        :param check_server: optional function to check if the server is ready
                             (default check method makes GET request to '/'
                              of HTTP endpoint)
        :return: the public port of the service exposed to host system if any
        """
        public_port = self.port_for(service, private_port)
        self.wait_until_responsive(
            timeout=30.0,
            pause=0.1,
            check=lambda: check_server(self.docker_ip, public_port),
        )
        return public_port

    def shutdown(self):
        self._docker_compose.execute('down', '-v')

    def port_for(self, service, port):
        """Get the effective bind port for a service."""

        # Lookup in the cache.
        cache = self._services.get(service, {}).get(port, None)
        if cache is not None:
            return cache

        output = self._docker_compose.execute(
            'port', service, str(port)
        )
        endpoint = output.strip()
        if not endpoint:
            raise ValueError(
                'Could not detect port for "%s:%d".' % (service, port)
            )

        # Usually, the IP address here is 0.0.0.0, so we don't use it.
        match = int(endpoint.split(':', 1)[1])

        # Store it in cache in case we request it multiple times.
        self._services.setdefault(service, {})[port] = match

        return match

    @staticmethod
    def wait_until_responsive(check, timeout, pause,
                              clock=timeit.default_timer):
        """Wait until a service is responsive."""

        ref = clock()
        now = ref
        while (now - ref) < timeout:
            if check():
                return
            time.sleep(pause)
            now = clock()

        raise Exception(
            'Timeout reached while waiting on service!'
        )


class DockerComposeExecutor(object):
    def __init__(self, compose_files, project_name):
        self._compose_files = compose_files
        self._project_name = project_name

    def execute(self, *subcommand):
        command = ["docker-compose"]
        for compose_file in self._compose_files:
            command.append('-f')
            command.append(compose_file)
        command.append('-p')
        command.append(self._project_name)
        command += subcommand
        return execute(command)


def docker_ip():
    """Determine IP address for TCP connections to Docker containers."""

    # When talking to the Docker daemon via a UNIX socket, route all TCP
    # traffic to docker containers via the TCP loopback interface.
    docker_host = os.environ.get('DOCKER_HOST', '').strip()
    if not docker_host:
        return '127.0.0.1'

    match = re.match('^tcp://(.+?):\d+$', docker_host)
    if not match:
        raise ValueError(
            'Invalid value for DOCKER_HOST: "%s".' % (docker_host,)
        )
    return match.group(1)


@pytest.fixture(scope='session')
def docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    """
    return [
        os.path.join(str(pytestconfig.rootdir), 'tests', 'docker-compose.yml')
    ]


@pytest.fixture(scope='session')
def docker_services(request, pytestconfig, docker_compose_files):
    """Provide the docker services as a pytest fixture.

    The services will be stopped after all tests are run.
    """
    keep_alive = request.config.getoption("--keepalive", False)
    project_name = "pytest{}".format(str(pytestconfig.rootdir))
    services = Services(docker_compose_files, project_name)
    yield services
    if not keep_alive:
        services.shutdown()


def pytest_addoption(parser):
    """Add custom options to pytest.

    Add the --keepalive option for pytest.
    """
    parser.addoption("--keepalive", "-K", action="store_true",
                     default=False, help="Keep docker containers alive")

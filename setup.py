import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.md')).read()

requires = [
    'pytest',
    'six'
]


def get_version():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION.txt")
    with open(p) as f:
        return f.read().strip()


setup(
    name='lovely-pytest-docker',
    version=get_version(),
    description='Pytest testing utilities with docker containers.',
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
    ],
    author='Lovely Systems',
    author_email='office@lovelysystems.com',
    url='https://github.com/lovelysystems/lovely-pytest-docker',
    keywords='pytest testing docker compose',
    namespace_packages=['lovely'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'pytest11': [
            'lovely_pytest_docker = lovely.pytest.docker.compose',
        ],
    },
)

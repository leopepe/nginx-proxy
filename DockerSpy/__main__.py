__author__ = 'leonardo'

from . import DockerSpy
from json import dumps

if __name__ == '__main__':
    docker = DockerSpy()
    container_env = docker.env
    print(dumps(container_env, indent=4))
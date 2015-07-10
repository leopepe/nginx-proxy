![nginx 1.9.0](https://img.shields.io/badge/nginx-1.9.0-brightgreen.svg) ![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# DockerSpy

This project implements an nginx balancer capable of automatcly include nodes behind it's reverse proxy as soon as they start on a same docker host. The proxy also can recoginize when one docker node is removed from the cluster. This behavior is guaranteed by DockerSpy app that listen to docker events.


## Usage

To start the container run the command as described:

    $ docker run -dt --name proxy -p 80:80 -p 443:443 -v /var/run/docker.sock:/var/run/docker.sock:ro -v /etc/nginx/certs/:/etc/nginx/certs:ro leopepe/nginx-proxy

In due to the nginx-proxy work correctly and recognize the nodes being bringup behind it the containers need to start with two environment variables:

VIRTUAL_HOST: Literally an unique virtual host name (vhost)
VIRTUAL_PORT: The port os the service running inside the docker container.

To start the containers "behind" the nginx-proxy:

    $ docker run -e VIRTUAL_HOST=node1.localhost -e VIRTUAL_PORT=8080 ...

Or by setting up the environment variable on the Dockerfile of your containers.

By now the project only supports single PORT services. If you intent to run services using multiple ports this project will not help you. Wait for next version or feel free to extend it. 

## Credits

This project was based on [jwilder/nginx-proxy][1] project

  [1]: https://github.com/jwilder/nginx-proxy

## TODO

1. Pydocs
2. Config parser.
3. Flexible template usage
4. System logging


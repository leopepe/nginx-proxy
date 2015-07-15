![nginx 1.9.0](https://img.shields.io/badge/nginx-1.9.0-brightgreen.svg) ![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# Nginx Reverse Proxy + DockerSpy

This project implements an nginx balancer capable of automatcly include nodes behind it's reverse proxy as soon as they start on a same docker host. The proxy also can recoginize when one docker node is removed from the cluster. This behavior is guaranteed by DockerSpy app that listen to docker events.

## Usage

To start the container run the command as described:

    $ docker run -dt --name proxy \
      -e 'PYTHONIOENCODING="utf-8"' \
      -p 80:80 -p 443:443 \
      -v /etc/nginx/certs:/etc/nginx/certs \
      -v /var/run/docker.sock:/var/run/docker.sock:ro \
      -v /app/templates:/app/templates leopepe/nginx-proxy:1.5

To a more flexible usage export the templates and certs directory containing your SSL certs and custom template files

You can also overwrite the dockerspy parameters and indicate a differente directory to save config files and template source:

    $ docker run -dt --name proxy \
      -e 'PYTHONIOENCODING="utf-8"' \
      -e 'ENV DOCKER_HOST="unix://var/run/docker.sock"' \
      -e 'CONFIG_DEST="/etc/nginx/conf.d/"' \
      -e 'TEMPLATE_FILE= "templates/node.nodomain.conf"' \
      ...

Note that the name `proxy` can also be changed to what suits you best

### Recognizing Cluster Members

In due to the nginx-proxy work correctly and recognize the nodes being bringup behind it the containers need to start with two environment variables:

VIRTUAL_HOST: Literally an unique virtual host name (vhost)
VIRTUAL_PORT: The port os the service running inside the docker container.

To start the containers "behind" the nginx-proxy:

    $ docker run -e VIRTUAL_HOST=node1.nodomain -e VIRTUAL_PORT=8080 ...

Or by setting up the environment variable on the Dockerfile of your containers.

By now the project only supports single PORT services. If you intent to run services using multiple ports this project will not help you. Wait for next version or feel free to extend it.

## Credits

This project was based on [jwilder/nginx-proxy][1] project

  [1]: https://github.com/jwilder/nginx-proxy

## TODO

- Extract dockerspy from proxy server

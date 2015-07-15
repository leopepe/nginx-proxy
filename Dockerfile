FROM leopepe/rproxy:1.0
MAINTAINER Leonardo Pepe leonardo.pepe@m4u.com.br

# Install wget and install/updates certificates
RUN apt-get update && \
    apt-get install -y -q --no-install-recommends \
    wget \
    python3 \
    python3-pip \
    unzip \
    git && \
    apt-get clean && \
    rm -r /var/lib/apt/lists/*

ENV PYTHONIOENCODING "utf-8"
ENV DOCKER_HOST "unix://var/run/docker.sock"
ENV CONFIG_DEST "/etc/nginx/conf.d/"
ENV TEMPLATE_FILE "templates/node.nodomain.conf"

# Generating ssl certs
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj '/CN=www.mydom.com/O=My Company Name LTD./C=US' \
    -keyout /etc/nginx/certs/nginx.key -out /etc/nginx/certs/nginx.crt

# Install honcho
RUN pip3 install honcho

# Copy app files
COPY ./app /app
COPY ./app/templates/default.conf /etc/nginx/conf.d/
COPY ./app/templates/nginx.conf /etc/nginx/nginx.conf

WORKDIR /app

RUN cd /app ; git clone https://github.com/leopepe/DockerSpy.git
RUN cd /app/DockerSpy ; python3 setup.py install

CMD ["honcho", "start"]

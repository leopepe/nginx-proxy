FROM nginx:1.9.2
MAINTAINER Leonardo Pepe leonardo.pepe@m4u.com.br

# Install wget and install/updates certificates
RUN apt-get update \
 && apt-get install -y -q --no-install-recommends \
    ca-certificates \
    wget \
    python3 \
    python-pip \
    unzip \
    libpcre3-dev \
    zlib1g-dev \
    libssl-dev \
    bsdtar \
    libldap2-dev
 && apt-get clean \
 && rm -r /var/lib/apt/lists/*

# Definig nginx version
ENV NGINX_VERSION 1.9.2

# use bsdtar for zip file
RUN curl -Ls https://github.com/kvspb/nginx-auth-ldap/archive/master.zip | bsdtar -xf- -C /tmp \
    && curl -s http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz | tar -xz -C /tmp \
	&& cd /tmp/nginx-${NGINX_VERSION} \
	&& ./configure --add-module=../nginx-auth-ldap-master --with-http_ssl_module --with-http_auth_request_module && make && make install

# Generating ssl certs
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/certs/nginx.key -out /etc/nginx/certs/nginx.crt

# Install Forego
RUN wget -P /usr/local/bin https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego \
 && chmod u+x /usr/local/bin/forego

COPY ./ /app
COPY ./default.conf /etc/nginx/conf.d/default.conf
WORKDIR /app

RUN pip install -r /app/venv/requirements.txt
RUN wget -P /app https://github.com/leopepe/DockerSpy/archive/master.zip \
 && unzip master.zip && chmod -R u+x DockerSpy-master/DockerSPy/__main__.py

CMD ["forego", "start", "-r"]

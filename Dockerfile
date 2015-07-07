FROM nginx:1.9.2
MAINTAINER Leonardo Pepe leonardo.pepe@m4u.com.br

# Install wget and install/updates certificates
RUN apt-get update \
 && apt-get install -y -q --no-install-recommends \
    ca-certificates \
    wget \
    python-pip \
    unzip \
 && apt-get clean \
 && rm -r /var/lib/apt/lists/*

# Install Forego
RUN wget -P /usr/local/bin https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego \
 && chmod u+x /usr/local/bin/forego

COPY ./ /app
COPY ./default.conf /etc/nginx/conf.d/default.conf
WORKDIR /app

RUN pip install -r /app/venv/requirements.txt
RUN wget -P /app https://github.com/leopepe/DockerSpy/archive/master.zip \
 && unzip master.zip && chmod -R u+x DockerSpy-master/DockerSPy/main.py

VOLUME ["/etc/nginx/certs"]

CMD ["forego", "start", "-r"]

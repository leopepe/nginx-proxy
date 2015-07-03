FROM nginx:1.9.2
MAINTAINER Leonardo Pepe leonardo.pepe@m4u.com.br

# Install wget and install/updates certificates
RUN apt-get update \
 && apt-get install -y -q --no-install-recommends \
    ca-certificates \
    wget \
    python3 \
    python-pip \
 && apt-get clean \
 && rm -r /var/lib/apt/lists/*

# Install Forego
RUN wget -P /usr/local/bin https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego \
 && chmod u+x /usr/local/bin/forego

COPY ./ /app
WORKDIR /app

RUN pip install -r /app/venv/requirements.txt

VOLUME ["/etc/nginx/certs"]

CMD ["forego", "start", "-r"]

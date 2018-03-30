FROM postgres

# Set the locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD transfer /app
RUN chmod 755 *

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -qq -y update && \
    apt-get -qq -y install \
    tar \
    git \
    tmux \
    curl \
    vim \
    dialog \
    net-tools \
    wget \
    build-essential \
    postgresql-server-dev-10 \
    libpq-dev \
    python \
    python-dev \
    python-distribute \
    python-pip && \
    rm -rf /var/lib/apt/list/*

RUN pip install -r /app/requirements.txt
RUN pg_createcluster 10 main --start
RUN chmod 777 /app
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
USER postgres

# Expose the ports
EXPOSE 5432 8000 8001

# Install packages
# ENV http_proxy http://10.33.50.14:8000
# ENV https_proxy http://10.33.50.14:8000

CMD ["/bin/sh","start.sh"]

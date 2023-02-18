ARG PYTHON_VERSION=3.8

FROM python:$PYTHON_VERSION

RUN pip install virtualenv
RUN python3 -m venv venv

WORKDIR /home/fenoman
COPY . .

RUN apt update
RUN apt-get install -y \
        build-essential \
        curl \
        default-libmysqlclient-dev \
        freetds-bin \
        freetds-dev \
        libaio1 \
        libecpg-dev \
        libffi-dev \
        libldap2-dev \
        libpq-dev \
        libsasl2-2 \
        libsasl2-dev \
        libsasl2-modules-gssapi-mit \
        libssl-dev \
        python3-dev \
        gcc

RUN apt-get clean

RUN groupadd fenomangroup && \
	useradd -U -G fenomangroup fenoman && \
    chown fenoman:fenoman /home/fenoman

RUN pip install --upgrade pip && \
	pip install --upgrade wheel && \
	pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8081 8090-8094
USER fenoman

ENTRYPOINT ["python3"]
CMD ["wsgi.py"]
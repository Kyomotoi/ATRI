FROM flyingjoe/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

ADD . /app/

EXPOSE 20000

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && rm -Rf /var/lib/apt/lists/* && apt-get update

RUN  apt install curl -y

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /usr/local/bin/python -m pip install  --no-cache-dir --upgrade --quiet pip

RUN poetry install

VOLUME /app/accounts /app/data

CMD poetry run python3 main.py
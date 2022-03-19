FROM flyingjoe/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"

COPY ./ /app/

RUN /usr/local/bin/python -m pip install  --no-cache-dir --upgrade --quiet pip \
    && pip install  --no-cache-dir --upgrade --quiet -r requirements.txt

VOLUME /app/accounts /app/data

CMD python3 main.py
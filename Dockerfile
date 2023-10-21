FROM sunpeek/poetry:py3.10-slim as base
# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    POETRY_VERSION=1.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base as base-builder
WORKDIR $PYSETUP_PATH
ADD ./poetry.lock ./pyproject.toml ./
RUN poetry install

FROM base as pre-production
EXPOSE 20000
COPY --from=base-builder $VENV_PATH /app/.venv/
COPY . /app/
VOLUME /app/accounts /app/data
WORKDIR /app

CMD poetry run python3 main.py
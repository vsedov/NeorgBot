FROM python:3.10-alpine

COPY poetry.lock pyproject.toml /app/

WORKDIR /app

ENV POETRY_VERSION=1.6.0

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry update --only main
RUN poetry env use python

COPY . .

CMD ["poetry", "run", "python3", "-m", "neorg"]

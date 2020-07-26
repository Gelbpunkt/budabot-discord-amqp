FROM docker.io/gelbpunkt/python:gcc10

RUN apk add --no-cache libgcc && \
    apk add --no-cache --virtual .build gcc musl-dev libffi-dev openssl-dev && \
    pip install --no-cache-dir poetry && \
    apk del .build && \
    adduser -S bot

USER bot
WORKDIR /bot

COPY pyproject.toml poetry.lock .

RUN poetry install --no-dev

COPY . .

CMD ["poetry", "run", "bot"]

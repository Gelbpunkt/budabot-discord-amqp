FROM python:3.8-alpine

WORKDIR /bot
COPY requirements.txt .

RUN apk add --virtual .build gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build && \
    adduser -S bot

USER bot

COPY . .

CMD ["python", "main.py"]

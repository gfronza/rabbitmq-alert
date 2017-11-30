FROM python:2-alpine

LABEL maintainer="milonas.ko@gmail.com"

RUN pip install --no-cache-dir rabbitmq-alert

CMD ["rabbitmq-alert"]

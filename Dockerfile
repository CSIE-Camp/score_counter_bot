# python discord bot
# Ubuntu 20.04
# Python 3.10

# Pull base image
FROM python:3.10

WORKDIR /app
COPY .env /app
COPY requirements.txt /app
COPY *.py /app
COPY cogs /app/cogs
COPY sample.json /app

RUN pip install -r requirements.txt
ENV DC_BOT_TOKEN=
ENV WEBHOOK_URL=

# run main.py & scoreboard.py
CMD ["python", "main.py"]
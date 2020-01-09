FROM python:alpine

LABEL Name=hangman Version=0.0.1

RUN adduser -D hangman

WORKDIR /Hangman

RUN find . -name '*.pyc' -delete

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY hangman.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP hangman.py

RUN chown -R hangman:hangman ./
USER hangman

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
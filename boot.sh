#!/bin/sh
source venv/bin/activate
echo "start upgrading database ."
flask db init
flask db migrate -m "users table"
flask db migrate -m "words table"
exec gunicorn -b :5000 --access-logfile - --error-logfile - hangman:app
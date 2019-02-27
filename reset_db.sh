#!/bin/bash

if [ "$1" == "makemigrations" ]; then
  rm darwin/migrations/00*.py
  python manage.py makemigrations
fi
rm db.sqlite3
touch db.sqlite3
python manage.py migrate
python manage.py dbseed


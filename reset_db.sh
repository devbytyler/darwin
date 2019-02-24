#!/bin/bash

if [ "$1" == "makemigrations" ]; then
  rm darwin/migrations/00*.py
  python manage.py makemigrations
fi
mysql -uroot -e "DROP DATABASE darwin"
mysql -uroot -e "CREATE DATABASE darwin"
python manage.py migrate
python manage.py dbseed
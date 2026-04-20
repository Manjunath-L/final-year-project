#!/usr/bin/env bash
set -o errexit

cd django-backend/concept_crafter
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

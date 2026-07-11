#!/bin/bash
set -euxo pipefail

echo "STEP 1: installing requirements"
pip install -r requirements.txt

echo "STEP 2: checking Django config"
python manage.py check

echo "STEP 3: checking for migrations"
python manage.py makemigrations --check --dry-run

echo "STEP 4: running migrations"
python manage.py migrate --no-input

echo "STEP 5: creating/updating admin user"
python manage.py bootstrap_admin

echo "STEP 6: collecting static files"
python manage.py collectstatic --no-input

echo "BUILD SCRIPT FINISHED"

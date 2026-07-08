#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true
python manage.py makemigrations
python manage.py migrate
echo "Bootstrap complete. Run: source .venv/bin/activate && python manage.py createsuperuser && python manage.py runserver"
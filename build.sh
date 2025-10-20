#!/usr/bin/env bash
set -o errexit

echo "Using Python version:"
python --version

pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

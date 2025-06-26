#!/usr/bin/env bash

# Install nodejs and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Python dependencies
pip install -r requirements.txt

# Django setup
python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

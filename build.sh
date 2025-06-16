#!/usr/bin/env bash

# Install nodejs and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Python dependencies
pip install -r requirements.txt

# Tailwind commands
python manage.py tailwind install
python manage.py tailwind build

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate

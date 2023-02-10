#!/bin/bash
set -eux

echo "POSTGRES_USER=heisenberg" >> .env
echo "POSTGRES_PASSWORD=iamthedanger" >> .env
echo "POSTGRES_DB=breakingbad" >> .env

echo "DEBUG = True" >> .env
secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe())")
echo "SECRET_KEY = \"$secret_key\"" >> .env
echo "DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]" >> .env
echo "SQL_ENGINE=django.contrib.gis.db.backends.postgis" >> .env
echo "SQL_DATABASE=breakingbad" >> .env
echo "SQL_USER=heisenberg" >> .env
echo "SQL_PASSWORD=iamthedanger" >> .env
echo "SQL_HOST=db" >> .env
echo "SQL_PORT=5432" >> .env
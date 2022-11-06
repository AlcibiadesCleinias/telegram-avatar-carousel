#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


if [ "$DEBUG" = "1" ]
then
    echo "Debug is True, lets makemigrations, migrate and create superuser..."
    python manage.py makemigrations
    python manage.py migrate
    echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
else
    echo "Debug is False, migrate and collectstatic..."
    python manage.py migrate
    python manage.py collectstatic --clear --noinput
fi

exec "$@"

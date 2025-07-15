#!/bin/sh

if [ "$DATABASE" = "postgres" ] 
then
    echo "Check if database is running..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "The database is up and running :-D"
fi

python manage.py makemigrations useraccount
python manage.py migrate useraccount

python manage.py makemigrations property
python manage.py migrate property

python manage.py makemigrations
python manage.py migrate

exec "$@"
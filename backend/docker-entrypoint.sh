#!/bin/sh

./wait-for-it.sh $DB_HOST:$DB_PORT

python manage.py migrate

if [ "$ENV" = "prod" ]; then

    mkdir -p ./logs
    touch ./logs/gunicorn-access.log

    python manage.py collectstatic --noinput --clear

    gunicorn config.wsgi:application \
        --bind 0.0.0.0:80 \
        --worker-tmp-dir /dev/shm \
        --workers=4 \
        --threads=8 \
        --log-file=- \
        --log-level=info \
        --worker-class=gthread \
        --access-logfile=./logs/gunicorn-access.log

fi

exec "$@"

#!/bin/sh
set -eu

printf "celery" > /tmp/container-role

if [ -z "${DATABASE_URL:-}" ]; then
    export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

postgres_ready() {
python << END
import sys
import psycopg

try:
    psycopg.connect(conninfo="${DATABASE_URL}")
except psycopg.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  echo 'Waiting for PostgreSQL to become available...' >&2
  sleep 1
done
echo 'PostgreSQL is available' >&2

python manage.py migrate --noinput
python manage.py compilemessages
python manage.py load_redis_index

# Install watchdog if not already installed
pip install watchdog[watchmedo]

# Start celery with watchdog
watchmedo \
    auto-restart --directory=./ --pattern=*.py --recursive -- \
    celery --workdir="/app" -A config.celery_app worker -B --loglevel=INFO

# printf "celery" > /tmp/container-role

# if [ -z "${DATABASE_URL}" ]; then
#     export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
# fi

# postgres_ready() {
# python << END
# import sys

# import psycopg

# try:
#     psycopg.connect(conninfo="${DATABASE_URL}")
# except psycopg.OperationalError as e:
#     print(e)
#     sys.exit(-1)
# sys.exit(0)

# END
# }

# until postgres_ready; do
#   >&2 echo 'Waiting for PostgreSQL to become available...'
#   sleep 1
# done
# >&2 echo 'PostgreSQL is available'

# python manage.py migrate --noinput
# python manage.py compilemessages
# python manage.py load_redis_index


# watchmedo \
#     auto-restart --directory=./ --pattern=*.py --recursive -- \
#     celery --workdir="/app" -A config.celery_app worker -B --loglevel=INFO

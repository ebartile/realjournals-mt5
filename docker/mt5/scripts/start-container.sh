#!/usr/bin/env bash
set -euo pipefail

# Execute pending migrations
echo Executing pending migrations
# wine python manage.py compilemessages
# wine python manage.py collectstatic --no-input
wine python -m pip install -r requirements.txt
wine python manage.py makemigrations
wine python manage.py migrate

# Start Real Journals processes
echo Starting Real Journals API...
if [ "$APP_ENV" == "production" ]; then
    exec gunicorn realjournals.wsgi:application \
        --name realjournals \
        --bind 0.0.0.0:8080 \
        --workers 3 \
        --worker-tmp-dir /dev/shm \
        --log-level=debug \
        --access-logfile - \
        "$@"
else
    exec wine python manage.py runserver 0.0.0.0:8080
fi

if [ "$APP_SCHEDULE" == "true" ]; then
	crontab /var/cron.schedule
	service cron restart
fi

if [ $# -gt 0 ]; then
	exec "$@"
else
	exec /usr/bin/supervisord --nodaemon \
		--configuration=/var/supervisord.conf \
		--logfile=/var/log/supervisord/supervisord.log \
		--logfile_maxbytes=5MB
fi


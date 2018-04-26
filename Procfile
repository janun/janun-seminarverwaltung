web: gunicorn config.wsgi:application
worker: celery worker --app=janun_seminarverwaltung.taskapp --loglevel=info

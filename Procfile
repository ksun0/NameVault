web: gunicorn NameVault.wsgi --log-file -
worker: celery -A NameVault worker -l info
beat: celery -A NameVault beat -l info

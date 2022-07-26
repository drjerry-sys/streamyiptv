web: gunicorn webScraper.wsgi --log-file -
worker: celery -A webScraper.celery worker -B --loglevel=info
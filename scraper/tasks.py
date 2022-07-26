import time
from celery import shared_task
from .scrapers import scrape


login_url = "https://mydash.one"
activityLogUrl = "https://mydash.one/rconnections"

@shared_task(max_retries=3)
def scrape_mydash():
    scrape(login_url, activityLogUrl)
    return 'task successfully done!'

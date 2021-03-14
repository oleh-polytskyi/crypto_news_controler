from crypto_news_app.celery_app import app as celery_app
from modules import ScrapinghubClientWrapper
from .models import NewsItem


@celery_app.task
def run_spider_task(spider):
    scrapy_client = ScrapinghubClientWrapper()
    scrapy_client.create_job(spider)


@celery_app.task
def write_items_to_db(spider):
    while True:
        scrapy_client = ScrapinghubClientWrapper()
        if list(scrapy_client.project.spiders.get(spider).jobs.iter_last()
                )[0]['state'] == 'finished':
            job_key = list(scrapy_client.project.spiders.get(spider)
                           .jobs.iter_last())[0]['key']
            items = scrapy_client.get_job_items(job_key)
            if items:
                list_of_objets = NewsItem.objects.filter(
                    title__in=[i['title'][0] for i in items]
                )
                for item in items:
                    if item['title'][0] in list(
                            list_of_objets.values_list('title', flat=True)):
                        continue
                    else:
                        db_item = NewsItem()
                        for key, value in item.items():
                            setattr(db_item, key, value[0])
                        db_item.save()
            break

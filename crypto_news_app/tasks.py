from crypto_news_app.celery_app import app as celery_app
from modules import ScrapinghubClientWrapper
from .models import NewsItem
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache


@celery_app.task()
def update_spiders_data(channel_name):

    spider_dict = cache.get('spiders_info')
    while True:
        new_spider_dict = ScrapinghubClientWrapper().get_spider_data()
        if new_spider_dict == spider_dict:
            time.sleep(15)
            continue
        else:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(channel_name,
                                              {"type": "chat.message",
                                               "text": new_spider_dict},
                                              )
            cache.set('spiders_info', new_spider_dict, 600)
            time.sleep(15)
    return {'status': 'finished'}


@celery_app.task
def run_spider_task(*args):
    scrapy_client = ScrapinghubClientWrapper()
    scrapy_client.create_job(args[0])


@celery_app.task
def write_items_to_db(*args):
    while True:
        scrapy_client = ScrapinghubClientWrapper()
        if list(scrapy_client.project.spiders.get(args[0]).jobs.iter_last()
                )[0]['state'] == 'finished':
            job_key = list(scrapy_client.project.spiders.get(args[0])
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

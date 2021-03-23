from channels.generic.websocket import AsyncJsonWebsocketConsumer
from modules.zyte_wrapper import ScrapinghubClientWrapper
from crypto_news_app.tasks import update_spiders_data
from django.core.cache import cache


class JobInfoConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.task_obj = update_spiders_data.delay(self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        self.task_obj.revoke()
        await self.close()

    async def receive(self, text_data):
        if cache.get('spiders_info'):
            data = cache.get('spiders_info')
        else:
            data = ScrapinghubClientWrapper().get_spider_data()
        await self.send_json(data)

    async def chat_message(self, event):
        await self.send_json(event['text'])


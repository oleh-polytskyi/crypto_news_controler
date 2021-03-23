from django.views import View
from django.shortcuts import render, redirect
from modules.zyte_wrapper import ScrapinghubClientWrapper
from django.core.cache import cache


class JobsInfoView(View):

    template_name = 'crypto_news_app/jobs_info.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if cache.get('spiders_info') is None:
                context = ScrapinghubClientWrapper().get_spider_data()
                cache.set('spiders_info', context, 600)

            else:
                context = cache.get('spiders_info')
            return render(request, self.template_name, {'context': context})
        else:
            return redirect('user_controller:log_in')


from django.core.exceptions import ValidationError
from django.http import JsonResponse
from modules import ScrapinghubClientWrapper
import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.shortcuts import render, redirect
from django.views import View


class RunSaveJobsView(View):

    template_name = 'crypto_news_app/run_jobs_save_data.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            scrapy_client = ScrapinghubClientWrapper()
            context = scrapy_client.get_list_of_spiders()
            return render(request, self.template_name, {'list_of_spider': context})
        else:
            return redirect('user_controller:log_in')


def ajaxsave(request):
    if request.user.is_authenticated:
        schedule_tmp = {}
        if request.POST.get('minute'):
            schedule_tmp['minute'] = request.POST.get('minute')
        else:
            schedule_tmp['minute']='*'
        if request.POST.get('hour'):
            schedule_tmp['hour'] = request.POST.get('hour')
        else:
            schedule_tmp['hour'] = '*'
        if request.POST.get('day_of_week'):
            schedule_tmp['day_of_week'] = request.POST.get('day_of_week')
        else:
            schedule_tmp['day_of_week'] = '*'

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=schedule_tmp['minute'],
            hour=schedule_tmp['hour'],
            day_of_week=schedule_tmp['day_of_week'],
            day_of_month='*',
            month_of_year='*'
        )
        for spider in dict(request.POST)['spiders[]']:
            try:
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,
                    name='run_spider_' + spider,
                    task='crypto_news_app.tasks.run_spider_task',
                    args=json.dumps([spider])
                )
            except ValidationError:
                task = PeriodicTask.objects.get(name="run_spider_" + spider)
                task.crontab = schedule
                task.save()
            try:
                PeriodicTask.objects.update_or_create(
                    crontab=schedule,
                    name='save_items_' + spider,
                    task='crypto_news_app.tasks.write_items_to_db',
                    args=json.dumps([spider])
                )
            except ValidationError:
                task = PeriodicTask.objects.get(name='save_items_' + spider)
                task.crontab = schedule
                task.save()
        return JsonResponse({'message': 'It worked fine'})
    else:
        return JsonResponse({'message': 'Permission denied'})




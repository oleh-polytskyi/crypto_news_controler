from django.views import View
from django.shortcuts import render, redirect


class JobsInfoView(View):

    template_name = 'crypto_news_app/jobs_info.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, {'context': 'context'})
        else:
            return redirect('user_controller:log_in')


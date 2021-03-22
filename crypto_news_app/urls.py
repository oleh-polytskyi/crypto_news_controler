from django.urls import path

from .views import RunSaveJobsView, ajaxsave, JobsInfoView

urlpatterns = [
    path('homepage/', RunSaveJobsView.as_view(), name='run_save_jobs'),
    path('ajaxsaved/', ajaxsave, name="ajaxsaved"),
    path('info/', JobsInfoView.as_view(), name='info')
]

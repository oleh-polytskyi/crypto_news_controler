from django.urls import path

from .views import RunSaveJobsView, ajaxsave

urlpatterns = [
    path('homepage/', RunSaveJobsView.as_view(), name='run_save_jobs'),
    path('ajaxsaved/', ajaxsave, name="ajaxsaved")
]

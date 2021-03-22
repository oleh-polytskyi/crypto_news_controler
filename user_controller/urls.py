from django.urls import path,re_path

from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('log_in/', CustomLoginView.as_view(), name='log_in'),
    path('log_out/', CustomLogoutView.as_view(), name='log_out'),
]

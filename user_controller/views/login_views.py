from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'user_controller/log_in.html'



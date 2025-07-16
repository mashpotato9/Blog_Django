from django.urls import path
from . import views

app_name = 'blogAuth'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('send_captcha', views.send_captcha, name='send_captcha'),
]
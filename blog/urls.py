from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('post', views.post_blog, name='post_blog'),
]
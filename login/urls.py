from django.conf.urls import url
from . import views

app_name = 'auth'
urlpatterns = [
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
]
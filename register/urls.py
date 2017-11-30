from django.conf.urls import url
from . import views

app_name = 'reg'
urlpatterns = [
    url(r'^$', views.reg, name='registration'),
]
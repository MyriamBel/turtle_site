from . import views
from django.conf.urls import url

app_name = 'articlesapp'
urlpatterns = [
    url(r'^article/get/(?P<article_id>\d+)/$', views.article, name='article'),
    url(r'^articles/addlike/(?P<article_id>\d+)/$', views.addlike, name='addlike'),
    url(r'^article/addcomment/(?P<article_id>\d+)/$', views.addcomment, name='addcomment'),
    url(r'^page/(\d+)/$', views.articles, name='articles'),
    url(r'^$', views.articles, name='articles'),
]
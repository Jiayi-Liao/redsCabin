from django.conf.urls import url

from . import views

app_name = 'redisView'
urlpatterns = [
    # ex: /polls/

    url(r'^$', views.index, name='index'),
    url(r'^newConn/$', views.newRedisConn, name='newConn'),
    url(r'^redisDetails/([0-9]+)/$', views.redisDetails, name='detail'),
    url(r'^redisSearch/([0-9]+)/$', views.redisKeySearch, name='searchByKey'),
    url(r'^redisKeyValues/([0-9]+)/$', views.redisKeyValues, name='redisKeyValues'),
    url(r'^redisCmd/([0-9]+)/$', views.redisCmd, name='redisCmd'),
]

from django.conf.urls import url

from . import views

app_name = 'redisView'
urlpatterns = [
    # ex: /polls/

    url(r'^$', views.index, name='index'),
    url(r'^newConn/$', views.newRedisConn, name='newConn'),
    url(r'^testConn/$', views.testRedisConn, name='testRedisConn'),
    url(r'^details/([0-9]+)/$', views.redisDetails, name='detail'),
    url(r'^search/([0-9]+)/$', views.redisKeySearch, name='searchByKey'),
    url(r'^KeyValues/([0-9]+)/$', views.redisKeyValues, name='redisKeyValues'),
    url(r'^cmd/([0-9]+)/$', views.redisCmd, name='redisCmd'),
]

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import RedisConn
from django.urls import reverse
import datetime
import redis
import json


# Create your views here.
def index(request):
    return render(request, 'redisView/index.html')


def newRedisConn(request):
    address = request.POST['address']
    port = request.POST['port']
    password = request.POST['password']
    redisConn = RedisConn(address=address, port=port, auth=password, pub_date=datetime.datetime.now())
    redisConn.save()
    return HttpResponseRedirect(reverse('redisView:detail', args=(redisConn.id,)))


def redisDetails(request, redisConn_id):
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    return render(request, 'redisView/mainUI.html', {'rd': redisConn})


def redisKeySearch(request, redisConn_id):
    key = request.GET['data']
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    r = redis.Redis(host=redisConn.address, port=redisConn.port, db=0, password=redisConn.auth)
    datas = r.execute_command('KEYS ' + key)
    return HttpResponse(json.dumps(datas))


def redisKeyValues(request, redisConn_id):
    key = request.GET['key']
    pageIndex = request.GET['pageIndex']
    pageSize = request.GET['pageSize']
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    r = redis.Redis(host=redisConn.address, port=redisConn.port, db=0, password=redisConn.auth)
    type = r.execute_command('TYPE ' + key)
    if type == 'string':
        data = r.execute_command('get ' + key)
    elif type == 'list':
        data = r.execute_command('lrange ' + key + ' 0 -1')
    elif type == 'set':
        data = r.execute_command('smembers ' + key)
    elif type == 'zset':
        data = r.execute_command('zrange ' + key + ' 0 -1 withscores')
    elif type == 'hash':
        data = r.execute_command('hgetall ' + key)
    return HttpResponse(json.dumps({"dataType": type, "datas": data}))


def redisCmd(request, redisConn_id):
    command = request.GET['command']
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    r = redis.Redis(host=redisConn.address, port=redisConn.port, db=0, password=redisConn.auth)
    try:
        data = r.execute_command(command)
    except:
        return HttpResponse("error")
    return HttpResponse("success")

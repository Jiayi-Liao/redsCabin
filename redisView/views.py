#coding=utf8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import RedisConn
from django.urls import reverse
import datetime
import redis
import json
from redisView.helpers import redis_helper
from django.template import Context, Template
from django.db import IntegrityError
import time

# Create your views here.
def index(request):
    objs = RedisConn.objects.all()
    return render(request, 'redisView/index.html', {"connList": objs})


def newRedisConn(request):
    address = request.POST['address']
    port = request.POST['port']
    password = request.POST['auth']
    status = redis_helper.testRedisConn(address, port, password)
    if status == 1:
        redisConn = RedisConn(address=address, port=port, auth=password, pub_date=datetime.datetime.now())
        try:
            redisConn.save()
            return HttpResponseRedirect(reverse('redisView:detail', args=(redisConn.id,)))
        except IntegrityError:
            desc = '连接已存在'
    return render(request, 'redisView/index.html', {'desc': desc if desc is not None else '连接错误'})


def testRedisConn(request):
    address = request.GET['address']
    port = request.GET['port']
    password = request.GET['auth']
    status = redis_helper.testRedisConn(address, port, password)
    return HttpResponse(json.dumps({"status": status}))


def redisDetails(request, redisConn_id):
    objs = RedisConn.objects.all()
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    return render(request, 'redisView/mainUI.html', {'rd': redisConn, 'connList': objs})


def redisKeySearch(request, redisConn_id):
    key = request.GET['data']
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    r = redis.Redis(host=redisConn.address, port=redisConn.port, db=0, password=redisConn.auth)
    start = int(time.time() % 100)
    datas = []
    if "*" in key:
        for i in range(1, 20, 1):
            rep = r.scan(start, key, 50000)
            start = rep[0]
            results = rep[1]
            print(start)
            if len(results) > 0:
                datas.extend(results)
    else:
        if r.exists(key):
            datas.append(key)
    if len(datas) > 100:
        datas = datas[:100]
    return HttpResponse(json.dumps(datas))


def redisKeyValues(request, redisConn_id):
    key = request.GET['key']
    pageIndex = request.GET['pageIndex']
    pageSize = request.GET['pageSize']
    redisConn = get_object_or_404(RedisConn, pk=redisConn_id)
    r = redis.Redis(host=redisConn.address, port=redisConn.port, db=0, password=redisConn.auth)
    type = r.execute_command('TYPE ' + key)
    if type == 'string':
        try:
            data = r.pfcount(key)
        except:
            data = r.execute_command('get ' + key)
    elif type == 'list':
        data = r.execute_command('lrange ' + key + ' 0 -1')
        if list(data) > 100:
            data = list(data)[:100]
    elif type == 'set':
        data = r.execute_command('smembers ' + key)
    elif type == 'zset':
        data = r.execute_command('zrange ' + key + ' 0 -1 withscores')
    elif type == 'hash':
        data = r.execute_command('hgetall ' + key)
        result = {}
        if len(data) > 100:
            for k in dict(data).keys()[:100]:
                result[k] = data[k]
        data = result
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

from django.contrib import admin

# Register your models here.
from .models import RedisConn

admin.site.register(RedisConn)

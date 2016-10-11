from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class RedisConn(models.Model):
    def __str__(self):
        return self.address

    address = models.CharField(max_length=200)
    port = models.CharField(max_length=200)
    auth = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date published')

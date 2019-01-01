from __future__ import unicode_literals

from django.db import models
import json

# Create your models here.
class Member(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    created_date = models.DateTimeField()

class BidItem(models.Model):
    name = models.CharField(max_length=50)
    data = models.CharField(max_length=1024)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def setdata(self, x):
        self.data = json.dumps(x)

    def getdata(self):
        return json.loads(self.data)

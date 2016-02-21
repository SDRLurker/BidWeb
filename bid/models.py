from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Member(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    created_date = models.DateTimeField()
    

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 13:33
from __future__ import unicode_literals

from django.db import migrations

from django.utils import timezone

def load_stores(apps, schema_editor):
    Store = apps.get_model("bid", "Member")
    store_admin = Store(id=u'admin', created_date=timezone.now())
    store_admin.save()

class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_stores),
    ]

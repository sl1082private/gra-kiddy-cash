# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 19:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baskets', '0004_auto_20170925_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='event',
        ),
    ]

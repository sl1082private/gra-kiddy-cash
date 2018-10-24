# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-22 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='date created')),
                ('last_modified', models.DateTimeField(verbose_name='date last modified')),
                ('is_complete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_touched', models.DateTimeField(verbose_name='date last touched')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=127, verbose_name='name of event')),
                ('event_date', models.DateField(verbose_name='date of event')),
                ('description', models.TextField(verbose_name='description of event')),
                ('created', models.DateTimeField(verbose_name='date created')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0, help_text='price in EUR')),
                ('created', models.DateTimeField(verbose_name='date created')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baskets.Basket')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=127, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=127, verbose_name='last_name')),
                ('vendor_number', models.IntegerField(default=0, help_text='Number assigned to vendor')),
                ('address', models.CharField(blank=True, default=None, max_length=127, null=True, verbose_name='address')),
                ('phone', models.CharField(blank=True, default=None, max_length=63, null=True, verbose_name='phone')),
                ('events', models.ManyToManyField(to='baskets.Event')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='vendorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baskets.Vendor'),
        ),
        migrations.AddField(
            model_name='currentevent',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baskets.Event'),
        ),
        migrations.AddField(
            model_name='basket',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baskets.Event'),
        ),
    ]

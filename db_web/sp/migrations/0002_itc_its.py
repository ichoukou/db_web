# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-13 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ITC',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ITS',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('salary', models.FloatField()),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-12 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BDT',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
            ],
        ),
    ]
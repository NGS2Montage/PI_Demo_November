# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recsys', '0017_auto_20180118_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='citation_only',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-11 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recsys', '0023_auto_20180611_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='pdf_url',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-11 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recsys', '0026_auto_20180611_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='citations',
            field=models.ManyToManyField(blank=True, through='recsys.CitationContext', to='recsys.Paper'),
        ),
    ]

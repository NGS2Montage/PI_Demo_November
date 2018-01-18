# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-17 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsys', '0011_auto_20180116_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitationContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='paper',
            name='citations',
        ),
        migrations.AddField(
            model_name='paper',
            name='cid',
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
        migrations.AddField(
            model_name='paper',
            name='fetched',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='citationcontext',
            name='from_paper_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_paper', to='recsys.Paper'),
        ),
        migrations.AddField(
            model_name='citationcontext',
            name='to_paper_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_paper', to='recsys.Paper'),
        ),
        migrations.AddField(
            model_name='paper',
            name='the_citations',
            field=models.ManyToManyField(blank=True, through='recsys.CitationContext', to='recsys.Paper'),
        ),
    ]
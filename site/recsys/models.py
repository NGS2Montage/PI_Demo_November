# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .managers import BuilderManager


class CitationObject(models.Model):

    doi = models.CharField(max_length=50, db_index=True)
    cite_data = models.TextField()

    objects = BuilderManager()

    class Meta:
        verbose_name = "CitationObject"
        verbose_name_plural = "CitationObjects"

    
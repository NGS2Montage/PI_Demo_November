# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.CitationObject)
class CitationObjectAdmin(admin.ModelAdmin):
    list_display = ["doi",]

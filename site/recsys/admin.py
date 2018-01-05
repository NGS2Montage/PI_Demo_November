# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.CitationObject)
class CitationObjectAdmin(admin.ModelAdmin):
    list_display = ["doi",]


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ["doi", "id", "title", "pdf"]


@admin.register(models.Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ["title", "cid", "record_id", "citation_only"]

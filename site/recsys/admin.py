# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models


# @admin.register(models.CitationObject)
# class CitationObjectAdmin(admin.ModelAdmin):
#     list_display = ["doi",]


@admin.register(models.Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ["get_doi_cid", "id", "title", "pdf"]

    def get_doi_cid(self, instance):
      return "{}/{}".format(instance.doi, instance.cid)


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
  pass


@admin.register(models.CitationContext)
class CitationContextAdmin(admin.ModelAdmin):
  pass


# @admin.register(models.Citation)
# class CitationAdmin(admin.ModelAdmin):
#     list_display = ["title", "cid", "record_id", "citation_only"]

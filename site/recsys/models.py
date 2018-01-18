# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlparse import urlparse, parse_qs

from django.apps import apps
from django.db import models

from .managers import BuilderManager


class CitationObject(models.Model):

    doi = models.CharField(max_length=50, db_index=True)
    cite_data = models.TextField()

    objects = BuilderManager()

    class Meta:
        verbose_name = "CitationObject"
        verbose_name_plural = "CitationObjects"


def pdf_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pdfs/<doi>.pdf
    return 'pdfs/{}.pdf'.format(instance.doi)


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Citation(models.Model):
    cid = models.CharField(max_length=50, db_index=True, unique=True)
    title = models.TextField()
    url = models.CharField(max_length=200)  # "/showciting?cid=11061"
    citation_only = models.BooleanField()
    author = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True, blank=True)
    context = models.TextField(null=True, blank=True)
    record = models.ForeignKey(
        'Paper',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.cid


class Paper(models.Model):
    doi = models.CharField(max_length=50, db_index=True, unique=True, blank=True, null=True)
    cid = models.CharField(max_length=50, db_index=True, unique=True, blank=True, null=True)
    title = models.TextField()
    abstract = models.TextField(blank=True)
    pdf_url = models.URLField(blank=True)
    pdf = models.FileField(upload_to=pdf_path, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    citations = models.ManyToManyField(
        'self',
        through='CitationContext',
        symmetrical=False,
        blank=True)
    year = models.IntegerField(null=True, blank=True)

    citation_only = models.BooleanField()
    # store whether we have tried to get all data for this thing yet
    fetched = models.BooleanField(default=False)

    def __str__(self):
        return "{}/{}".format(self.doi, self.cid)


class CitationContext(models.Model):
    from_paper = models.ForeignKey(Paper, related_name='from_paper')
    to_paper = models.ForeignKey(Paper, related_name='to_paper')
    context = models.TextField(blank=True)
    
    def __str__(self):
        return "{} cites {}".format(self.from_paper_id, self.to_paper_id)

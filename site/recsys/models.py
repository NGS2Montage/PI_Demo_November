# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import requests

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models, transaction
from django.db.models import Q

from .managers import BuilderManager
from .utils import cid_from_url, doi_from_url, stir_the_soup, MissingDataException, start_from_next_url


logger = logging.getLogger('recsys.models')


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

    def __unicode__(self):
        return u'{}'.format(self.name)


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
    url = models.URLField(blank=True)
    next_url = models.URLField(blank=True)
    pdf = models.FileField(upload_to=pdf_path, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    citations = models.ManyToManyField(
        'self',
        through='CitationContext',
        symmetrical=False,
        blank=True)
    year = models.IntegerField(null=True, blank=True)

    citation_only = models.BooleanField(default=False)
    # store whether we have tried to get all data for this thing yet
    fetched = models.BooleanField(default=False)
    fetched_co_citations = models.BooleanField(default=False)
    added_to_db = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}/{}".format(self.doi, self.cid)

    def __unicode__(self):
        return u"{}/{}".format(self.doi, self.cid)

    @transaction.atomic
    def add_authors(self, authors):
        for author in authors:
            if not self.authors.filter(name__iexact=author).exists():
                a, created = Author.objects.get_or_create(
                    defaults={'name': author},
                    name__iexact=author
                )
                self.authors.add(a)

    @classmethod
    def create_from_doi(cls, doi):
        paper, created = Paper.objects.get_or_create(doi=doi)
        return paper.create_from_viewdoc({
            'doi': doi
        })

    def fetch(self):
        if self.citation_only:
            self.create_from_showciting(self.cid)
        else:
            if self.doi:
                self.create_from_viewdoc({
                    'doi': self.doi
                })
            elif self.cid:
                self.create_from_viewdoc({
                    'cid': self.cid
                })
            else:
                logger.error("Neither doi or cid is set for pk={}".format(self.pk))

    def create_from_showciting(self, cid):
        if self.next_url:
            self.fetch_next()
            return

        url = "http://citeseerx.ist.psu.edu/showciting"
        payload = {"cid": cid}

        (response, soup) = stir_the_soup(url, payload)

        # paper, created = Paper.objects.get_or_create(cid=cid_from_url(response.url))
        # self.fetched = True

        title = soup.h2.string.strip()
        if len(title) >= 6 and title[-1] == ")" and title[-6] == "(":
            self.year = title[-5:-1]
            title = title[:-6].strip()
        self.title = title

        venue = soup.find(id="docVenue")
        if venue:
            self.venue = venue.find_all('td')[1].string

        authors = soup.find(id="docAuthors")
        if authors:
            authors = authors.string.strip()[len("by "):].split(", ")

        self.add_authors(authors)
        self.fetch_citing(soup)

        self.save()

    def fetch_next(self):
        start_param = start_from_next_url(self.next_url)

        url = "http://citeseerx.ist.psu.edu/showciting"
        payload = {
            "cid": self.cid,
            "sort": "cite",
            "start": start_param
        }

        (response, soup) = stir_the_soup(url, payload)
        self.fetch_citing(soup)

        self.save()

    def fetch_citing(self, soup):
        divs = soup.find_all('div', class_='result')
        next_page = soup.find(id="pager")

        if not next_page.a:
            self.fetched = True
        else:
            self.next_url = next_page.a.attrs['href']

        for div in divs:
            citation_paper, context = self.create_from_citing_div(div)
            if citation_paper:
                CitationContext.objects.get_or_create(
                    from_paper=citation_paper,
                    to_paper=self,
                    context=context if context else "")

    def create_from_citing_div(self, div):
        url = div.h3.a.attrs['href']
        doi = doi_from_url(url)

        if not doi:
            logger.debug("doi is missing in {} from {}".format(url, self))
            return None, None

        paper, created = Paper.objects.get_or_create(doi=doi)

        paper.title = div.h3.a.string.strip()

        authors = []
        info = div.find(class_="pubinfo")
        if info:
            authors = info.find(class_="authors")
            if authors:
                authors = [a.strip() for a in authors.string[len('by '):].strip().split(', ')]

            venue = info.find(class_="pubvenue")
            if venue:
                paper.venue = venue.string[len('- '):]

            year = info.find(class_="pubyear")
            if year:
                paper.year = year.string[len(', '):]

        abstract = div.find(class_="pubabstract")
        if abstract:
            paper.abstract = abstract.string.strip()

        context = div.select('p.citationContext')
        if context:
            context = context[0].string.strip()

        paper.save()
        if authors:
            paper.add_authors(authors)

        return paper, context

    def subsume(self, other):
        for cc in CitationContext.objects.filter(from_paper=other):
            if not CitationContext.objects.filter(from_paper=self, to_paper=cc.to_paper).exists():
                cc.from_paper = self
                cc.save()

        for cc in CitationContext.objects.filter(to_paper=other):
            if not CitationContext.objects.filter(to_paper=self, from_paper=cc.from_paper).exists():
                cc.to_paper = self
                cc.save()

        other.delete()

    def create_from_viewdoc(self, payload):
        url = "http://citeseerx.ist.psu.edu/viewdoc/versions"

        (response, soup) = stir_the_soup(url, payload)

        # paper, created = Paper.objects.get_or_create(doi=doi_from_url(response.url))
        doi = doi_from_url(response.url)

        # so, if self is a cid based one we might have new info about our
        # doi here, in fact, that doi could already be in the DB, in which
        # case, merge? delete myself?? idk?
        existing = Paper.objects.filter(~Q(pk=self.pk), doi=doi)
        if existing.exists():
            better = existing.first()
            better.cid = self.cid
            better.subsume(self)
            better.save()
            return
            # self.subsume(existing.first())  # there really shouldn't be more than one
            # self.save()
            # return

        # otherwise, just update this one
        self.doi = doi
        self.citation_only = False
        self.fetched = True

        authors = []
        for tr in soup.find_all('tr'):
            if tr.td:
                datum = tr.td.string.lower()

                if datum == "title":
                    self.title = tr.find_all('td')[1].string.strip()
                elif datum == "abstract":
                    self.abstract = tr.find_all('td')[1].string.strip()
                elif datum == "year":
                    self.year = tr.find_all('td')[1].string.strip()
                elif datum == "venue":
                    self.venue = tr.find_all('td')[1].string.strip()
                elif datum == "author name":
                    authors.append(tr.find_all('td')[1].string.strip())

        self.add_authors(authors)

        try:
            self.fetch_citations()
        except MissingDataException as e:
            logger.error(e)

        self.fetch_cocitations()
        self.download_pdf()
        self.save()

    def fetch_citations(self):
        if not self.doi:
            raise MissingDataException("Need doi set to fetch_citations {}".format(self))

        url = "http://citeseerx.ist.psu.edu/viewdoc/citations"
        payload = {'doi': self.doi}

        _, soup = stir_the_soup(url, payload)
        citation_table = soup.find(id="citations").table
        if citation_table is not None:
            for tr in citation_table.find_all('tr'):
                citation_paper, context = self.handle_one_citation(tr)
                CitationContext.objects.get_or_create(
                    from_paper=self,
                    to_paper=citation_paper,
                    context=(context if context else ""))
        else:
            raise MissingDataException("No citation table".format(self))

    def handle_one_citation(self, tr):
        td = tr.find_all('td')[1]
        attrs = td.a.attrs

        url = attrs['href']

        paper, _ = Paper.objects.get_or_create(cid=cid_from_url(url))
        # if paper.fetched:
        #     return

        paper.title = td.a.string
        paper.url = url
        paper.citation_only = ('showciting' in url)

        # hoping that contents[2] will always be the author/year string
        author_year = td.contents[2].string.split() if len(td.contents) > 2 else []

        # [u'-', u'Baumeister,', u'Leary', u'-', u'1995']
        if author_year and author_year[0] == '-':
            next_dash = author_year.index('-', 1) if '-' in author_year[1:] else len(author_year)

            # don't use author, it's pretty trashy
            # author = ' '.join(author_year[1:next_dash])
            paper.year = author_year[next_dash + 1] if next_dash + 1 < len(author_year) else None

        context = td.select('p.citationContext')
        if context:
            context = context[0].string.strip()

        paper.save()
        return paper, context

    def fetch_cocitations(self):
        url = "http://citeseerx.ist.psu.edu/viewdoc/similar"
        payload = {
            "doi": self.doi,
            "type": "cc"
        }

        (response, soup) = stir_the_soup(url, payload)
        table = soup.find(class_="refs")

        if table is not None:
            for tr in table.find_all('tr'):
                score = tr.find(class_="title")
                if score:
                    score = score.string.strip()
                else:
                    continue

                try:
                    score = int(score)
                except ValueError:
                    continue

                co_paper, _ = self.handle_one_citation(tr)
                CoCitation.objects.get_or_create(
                    co_from_paper=self,
                    co_to_paper=co_paper,
                    score=score)

    def download_pdf(self):
        pdf_url = "http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf".format(self.doi)
        response = requests.get(pdf_url)

        if response.status_code != 200:
            logger.error('ERROR code {} for PDF at {}'.format(response.status_code, pdf_url))
            raise MissingDataException("No PDF for {}".format(self))

        self.pdf = SimpleUploadedFile(
            self.doi,
            response.content,
            content_type="application/pdf")


class CoCitation(models.Model):
    co_from_paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='co_from_paper')
    co_to_paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='co_to_paper')
    score = models.IntegerField()

    def __str__(self):
        return "{} co-cited with {}".format(self.co_from_paper, self.co_to_paper)

    def __unicode__(self):
        return u"{} co-cited with {}".format(self.co_from_paper, self.co_to_paper)


class CitationContext(models.Model):
    from_paper = models.ForeignKey(Paper, related_name='from_paper')
    to_paper = models.ForeignKey(Paper, related_name='to_paper')
    context = models.TextField(blank=True)

    def __str__(self):
        return '"{}" -> "{}"'.format(self.from_paper, self.to_paper)

    def __unicode__(self):
        return u'"{}" -> "{}"'.format(self.from_paper, self.to_paper)

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q

import logging
import requests

from .models import Paper, Author, Citation, CitationContext
from .scripts.scraper import Record


logger = logging.getLogger('recsys.forms')


class CitationForm(forms.ModelForm):
    class Meta:
        model = Citation
        fields = [
            'cid',
            'title',
            'url',
            'citation_only',
            'author',
            'year',
            'context',
        ]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", ]


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = [
            'doi',
            'cid',
            'title',
            'abstract',
            'pdf_url',
            'pdf',
            'venue',
            'authors',
            'citation_only',
            'fetched',
            'year'
        ]

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.fields['authors'].to_field_name = 'name'


def add_authors(authors):
    records_added = 0
    errors = []

    for author in authors:
        form = AuthorForm({'name': author})
        if form.is_valid():
            # Row data is valid so save the author.
            _, created = Author.objects.get_or_create(**form.cleaned_data)

            if created:
                records_added += 1
        else:
            errors.append(form.errors)

    return records_added, errors


def fetch_pdf(doi, pdf_url):
    response = requests.get(pdf_url)

    return SimpleUploadedFile(
        doi,
        response.content,
        content_type="application/pdf")


def add_citations(from_paper, record):
    records_added = 0

    for citation in record['citations']:
        if 'authors' in citation:
            added, _ = add_authors(citation['authors'])
            records_added += added

        query = Q()
        if 'cid' in citation:
            query = query | Q(cid=citation['cid'])
        if 'doi' in citation:
            query = query | Q(doi=citation['doi'])

        to_paper = Paper.objects.filter(query)
        if to_paper.exists():
            to_paper = to_paper[0]
        else:
            form = PaperForm(citation)
            if form.is_valid():
                to_paper = form.save()
                records_added += 1
            else:
                logger.error("Could not save citation {} {}".format(citation, form.errors))
                break

        _, created = CitationContext.objects.get_or_create(
            from_paper=from_paper,
            to_paper=to_paper,
            context=citation['context'] if 'context' in citation else "")
        if created:
            records_added += 1
    return records_added


def follow_citation(paper):
    record = Record(paper.cid, 'cid', paper.citation_only)

    if hasattr(record, 'title'):
        paper.title = record.title
    if hasattr(record, 'venue'):
        paper.venue = record.venue
    if hasattr(record, 'year'):
        paper.year = record.year

    if not paper.citation_only:
        paper.doi = record.doi
        paper.abstract = record.abstract
        paper.pdf_url = record.pdf_url
        paper.pdf = fetch_pdf(record.doi, record.pdf_url)

    paper.fetched = True
    paper.save()

    records_added = add_citations(paper, record.toJSON())
    return records_added


def add_paper(record):
    paper = None
    records_added, errors = add_authors(record['authors'])

    # Get the pdf
    record_files = {
        'pdf': fetch_pdf(record['doi'], record['pdf_url'])
    }

    record['citation_only'] = False
    record['fetched'] = True
    form = PaperForm(record, record_files)
    if form.is_valid():
        # Row data is valid so save the record.
        paper = form.save()
        records_added += 1

        records_added += add_citations(paper, record)
    else:
        errors.append(form.errors)

    return records_added, errors, paper

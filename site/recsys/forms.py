from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

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
        to_paper = Paper.objects.filter(cid=citation['cid'])
        if to_paper.exists():
            to_paper = to_paper[0]
        else:
            form = PaperForm(citation)
            if form.is_valid():
                to_paper = form.save()
                records_added += 1
            else:
                logger.error("Could not save citation {}".format(citation))

        CitationContext.objects.create(
            from_paper=from_paper,
            to_paper=to_paper,
            context=citation['context'] if 'context' in citation else "")
        records_added += 1
    return records_added


def follow_citation(paper):
    record = Record(paper.cid, 'cid')

    paper.doi = record.doi
    paper.title = record.title
    paper.abstract = record.abstract
    paper.venue = record.venue
    paper.fetched = True
    paper.year = record.year
    paper.pdf_url = record.pdf_url

    paper.pdf = fetch_pdf(record.doi, record.pdf_url)
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

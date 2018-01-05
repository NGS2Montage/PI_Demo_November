from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

import logging
import requests

from .models import Paper, Author, Citation

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
            'title',
            'abstract',
            'pdf_url',
            'pdf',
            'venue',
            'authors',
            'year'
        ]

    def __init__(self, *args, **kwargs):
        super(PaperForm, self).__init__(*args, **kwargs)

        self.fields['authors'].to_field_name = 'name'


def add_paper(record):
    paper = None
    records_added = 0
    errors = []

    for author in record['authors']:
        form = AuthorForm({'name': author})
        if form.is_valid():
            # Row data is valid so save the record.
            _, created = Author.objects.get_or_create(**form.cleaned_data)

            if created:
                records_added += 1
        else:
            errors.append(form.errors)

    # Get the pdf
    response = requests.get(record['pdf_url'])
    record['pdf'] = record['doi']

    record_files = {
        'pdf': SimpleUploadedFile(
            record['doi'],
            response.content,
            content_type="application/pdf")
    }

    form = PaperForm(record, record_files)
    if form.is_valid():
        # Row data is valid so save the record.
        paper = form.save()
        records_added += 1

        for citation in record['citations']:
            qs = Citation.objects.filter(cid=citation['cid'])

            if qs.exists():
                logger.debug("Citation {} for {} already exists".format(qs[0].cid, paper.doi))
                paper.citations.add(qs[0])
            else:
                form = CitationForm(citation)
                if form.is_valid():
                    _, created = paper.citations.get_or_create(**form.cleaned_data)

                    if created:
                        records_added += 1
                else:
                    errors.append(form.errors)
    else:
        errors.append(form.errors)

    return records_added, errors, paper

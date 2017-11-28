import json

from django.db import models

from main import fetch_data_helper


class BuilderManager(models.Manager):
    def get_or_build(self, doi, *args, **kwargs):
        r = self.filter(doi=doi, *args, **kwargs)
        if r.exists():
            print("Found {} in DB".format(doi))
            return r[0]

        print("No {} - building".format(doi))
        cite_data = fetch_data_helper(doi)
        return self.create(doi=doi, cite_data=json.dumps(cite_data))

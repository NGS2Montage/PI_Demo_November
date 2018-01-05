# To run locally

1. Start virtualenv, if you're into that
1. `pip install -r requirements.txt`
1. `./manage.py migrate`
1. `./manage.py runserver`
1. Go to your browser, browse to `localhost:8000`


# To use Recommender System DB

You could connect to the DB yourself and run raw SQL but I recommend using Django's objects. There is some example code below (run this from the `site/` directory):

## Architecture

1. `Paper` objects represent a CiteSeerX record for a publication. They have a `pdf` FileField which can be opened for access to the PDF of the publication. (Also, pdfs are stored in `site/montage/media/<doi>_<random_letters>.pdf`).

1. The `citations` field for a `Paper` object is not a full record for each cited publication. If the full record for a citation has been scraped, the citation's `record` field will be the ID of a `Paper` object for the publication. Otherwise, `citation.record` will be `None`. 

1. `Citation` objects do not have PDFs. Only `Paper`s do.

```
# Need these lines to use any Django stuff
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings")
django.setup()


from recsys.models import *

all_papers = Paper.objects.all()
paper = all_papers[0]

print(paper.doi + " " + paper.title)
# Check out the Paper class in site/recsys/models.py for all the data a paper has

citations = paper.citations.all()
citation = citations[0]

# citeseerx identifies citation by cid (not doi)
print(citation.cid + " " + citation.title)

# Likewise, check out the Citation class in site/recsys/models.py


if citation.record is not None:
    cited_paper = citation.record
```

## Scripts for Scraping

1. Add a paper to the database with:

```
./manage.py runscript collect_paper --script-args 10.1.1.874.7127
```

This will add exactly one `Paper` to the database and one `Citation` for each publication listed on that paper's citations page on CiteSeerX. We will not have PDFs for the Citations, only for the Paper.

2. Fetch PDFs for citations (where possible):

```
./manage.py runscript follow_citations --script-args 10.1.1.874.7127
```

This will make `Paper` objects for each paper that `10.1.1.874.7127` cites that is in CiteSeerX. 

If you don't care about a particular Paper and just want to follow every possible Citation, omit the DOI:

```
# follow every citation
./manage.py runscript follow_citations
```


## A Note on `citation_only`

Some citations are not in CiteSeerX. In these cases, we cannot get PDFs for those citations since CiteSeerX hasn't indexed them. These cases are called `citation_only` meaning that CiteSeerX only has a record that this is cited not a record of the actual publication.

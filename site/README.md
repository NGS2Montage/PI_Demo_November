# To run locally

1. Start virtualenv, if you're into that
1. `pip install -r requirements.txt`
1. `./manage.py migrate`
1. `./manage.py runserver`
1. Go to your browser, browse to `localhost:8000`


# To access data

Three possible ways...

1. Browse the Papers on the Django admin page (get a superuser account from Nathan for this).
1. Use Django ORM for queries. Example:
    ```
    # Need these lines to use any Django stuff
    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings")
    django.setup()


    from recsys.models import *

    all_papers = Paper.objects.all()
    ```
3. Raw SQL. If Nathan has made you a psql account already all you need to do is `psql -d django_db`

The only tables that have an data are 
* `recsys_paper`
* `recsys_citationcontext` which has the many-to-many mappings from citing paper to cited paper
* `recsys_author`
* `recsys_paper_authors` which has the many-to-many mappings from Paper to Author

## Paper table

| Column        | Meaning           |
| ------------- | ------------- | 
| `doi` | doi |
| `cid` | Papers that citeseer doesn't know about will only have `cid` but no `doi` |
| `title` | |
| `abstract` | |
| `venue` | |
| `year` | |
| `pdf` | Path to the actual PDF stored in `montage/media/pdfs`, Django ORM can just open this like a file |
| `citation_only` | (Scraper only) True if CiteSeer only has the citation for this paper and not the pdf Ø|
| `pdf_url` | (Scraper only) URL from the "Download PDF" button on citeseer |
| `fetched` | (Scraper only) True if we have already scraped the page for this paper and added all its citations |
| `authors` | (Django ORM only) QuerySet of authors that go with this paper |
| `citations` | (Django ORM only) QuerySet of Papers that this paper cites |

## A Note on `citation_only`

Some citations are not in CiteSeerX. In these cases, we cannot get PDFs for those citations since CiteSeerX hasn't indexed them. These cases are called `citation_only` meaning that CiteSeerX only has a record that this is cited not a record of the actual publication.

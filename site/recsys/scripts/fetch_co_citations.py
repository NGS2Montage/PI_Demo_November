from recsys.models import Paper
from recsys.forms import get_co_citations


def run(doi=None):
    for paper in Paper.objects.filter(fetched=True, fetched_co_citations=False):
        try:
            get_co_citations(paper)
        except Exception as e:
            print("This didn't work for some reason, carrying on anyway")

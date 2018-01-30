from recsys.models import Paper
from recsys.forms import follow_citation


def run(doi='10.1.1.598.8940'):
    p = Paper.object.get(doi=doi)

    for c in p.citations.all():
        for cc in c.citations.filter(fetched=False):
            if not cc.fetched:
                print("Might need {}".format(cc))
                follow_citation(cc)
            else:
                print("Do not need {}".format(cc))

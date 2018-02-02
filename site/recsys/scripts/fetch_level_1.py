from recsys.models import Paper
from recsys.forms import follow_citation


def run(doi=None):
    if doi is not None:
        dois = [doi]
    else:
        dois = ["10.1.1.165.3572", "10.1.1.675.4811", "10.1.1.656.6724", "10.1.1.874.7127", "10.1.1.893.9921", "10.1.1.318.9608", "10.1.1.210.4690", "10.1.1.1010.4992", "10.1.1.815.6479", "10.1.1.152.23", "10.1.1.15.1034", "10.1.1.594.9165", "10.1.1.21.9786", "10.1.1.211.1697", "10.1.1.545.6095", "10.1.1.625.6731", "10.1.1.897.3569", "10.1.1.979.9766", "10.1.1.22.8200", "10.1.1.198.5074", "10.1.1.295.6783", "10.1.1.404.4956", "10.1.1.25.5747", "10.1.1.475.18",]

    for doi in dois:
        p = Paper.objects.filter(doi=doi)
        if p.exists():
            p = p[0]
        else:
            print("No such paper in DB {}".format(doi))
            continue

        for c in p.citations.filter(fetched=False):
            if not c.fetched:
                print("Might need {}".format(cc))
                follow_citation(cc)
            else:
                print("Do not need {}".format(cc))

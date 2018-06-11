import requests
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs


class MissingDataException(Exception):
    pass


def cid_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['cid'][0] if 'cid' in qs and qs['cid'] else None


def doi_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['doi'][0] if 'doi' in qs and qs['doi'] else None


def start_from_next_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['start'][0] if 'start' in qs and qs['start'] else None


def stir_the_soup(url, payload):
    response = requests.get(url, params=payload)

    if response.status_code != 200:
        logger.error('ERROR code {} for {}'.format(response.status_code, payload))
        raise MissingDataException("Record {} {}".format(response.status_code, payload))

    return (response, BeautifulSoup(response.content, "html.parser"))

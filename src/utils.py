import os
import constants
from urlparse import urlparse
import requests


constants.csx_paper_url

def get_doi_from_url(url):
    res = None
    try:
        parser = urlparse(url)
        query = parser.query
        query_parts = query.split('&')
        for qp in query_parts:
            fragments = qp.split('=')
            if fragments[0] == 'doi' :
                res = fragments[1]
            return res
    except:
        print('Malformed URL or No doi query parameter!')
    return None

def _validate_doi(doi):
    url = constants.csx_paper_url
    url = url.replace ('__DOI__', doi)
    r = requests.get (url)
    return r.status_code == 200
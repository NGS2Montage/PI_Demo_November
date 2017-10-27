import os
import constants
from urlparse import urlparse
import requests


cwd = None

def get_url(doi):
    url = constants.csx_paper_url
    url = url.replace ('__DOI__', doi)
    return url


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


def nav_to_data_dir():
    global cwd
    cwd = os.getcwd()
    os.chdir (constants.data_dir_location)
    os.chdir (constants.data_dir)
    return

def nav_to_op_dir():
    global cwd 
    cwd = os.getcwd()
    os.chdir (constants.op_dir_location)
    os.chdir (constants.op_dir)
    return


def nav_to_src():
    global cwd
    os.chdir (cwd)
    return


def validate_doi(doi):
    url = constants.csx_paper_url
    url = url.replace ('__DOI__', doi)
    r = requests.get (url)
    return r.status_code == 200

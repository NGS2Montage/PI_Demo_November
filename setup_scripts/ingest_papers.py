import sys
import xmltodict
import json
import os
import glob
from joblib import Parallel, delayed

sys.path.append ("./../.")
from src import mongoDBI
from src import constants

db_name = constants.db_name
table = constants.papers_table
dbi = None
num_parallel = 15


def write_doc_to_db(key, paper_dict):
    global db_name
    dbi = mongoDBI.mongoDBI (db_name=db_name)
    key_label = constants.paper_key_label
    key_contents = key
    value_label = constants.value_label
    value_contents = paper_dict
    dbi.insert_obj (table, key_label, key_contents, value_label, value_contents)
    return


def process_xml(file_name):
    with  open (file_name) as f:
        doc = xmltodict.parse (f.read ())

    if doc is None:
        return None

    top_node = doc['paper']

    if top_node is None:
        return None

    doi = top_node['doi']
    print '>', doi

    write_doc_to_db (doi, top_node)
    return;


def process_all():
    cwd = os.getcwd ()
    file_loc = 'data_dir/papers/'
    os.chdir ("../" + file_loc)
    files = glob.glob ("*.xml")
    # print files
    global num_parallel
    Parallel (n_jobs=num_parallel) (delayed (process_xml) (file_name) for file_name in files)
    os.chdir (cwd)
    return


def test_sample():
    dbi = mongoDBI.mongoDBI (db_name=db_name)
    key_label = constants.paper_key_label
    key_contents = '10.1.1.127.3891'
    value_label = constants.value_label
    z = dbi.find (table, key_label, key_contents, value_label)
    print z


# ----------------------- #

process_all ()
test_sample ()

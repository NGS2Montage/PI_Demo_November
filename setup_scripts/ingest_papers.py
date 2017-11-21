import sys
import xmltodict
import json
import os
import glob

sys.path.append ("./../.")
from src import mongoDBI
from src import constants

db_name = constants.db_name
table = constants.papers_table
dbi = None
dbi = mongoDBI.mongoDBI (db_name=db_name)


def write_doc_to_db(key, paper_dict):
    global dbi, table
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

    paper_dict = {}

    title = top_node['title']
    paper_dict['title'] = title

    author = top_node['author']
    paper_dict['author'] = author

    doi = top_node['doi']
    paper_dict['doi'] = doi

    abstract = top_node['abstract']
    paper_dict['abstract'] = abstract

    key = top_node['key']
    paper_dict['key'] = key

    paper_dict['citations'] = []
    citation_node = top_node['citations']['citation']
    count = len (citation_node)

    for i in range (count):
        data = citation_node[i]
        paper_dict['citations'].append (data)

    write_doc_to_db (doi, paper_dict)


def process_all():
    cwd = os.getcwd ()
    file_loc = 'data_dir/papers/'
    os.chdir ("../" + file_loc)
    files = glob.glob ("*.xml")
    print files
    file_name = '10.1.1.61.2545.xml'
    process_xml (file_name)
    os.chdir (cwd)
    return

process_all()
#
# key_label = constants.paper_key_label
# key_contents = '10.1.1.61.2545'
# value_label =  constants.value_label
# z = dbi.find(table, key_label, key_contents, value_label)

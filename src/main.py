import argparse
import constants
import os
import requests
import utils
import mongoDBI
import xmltodict
import json


def fetch_all_info_from_xml(file_name):
    doc = None
    with  open (file_name) as f:
        doc = xmltodict.parse (f.read ())

    if doc is None:
        return None

    cit_context = []
    top_node = doc['paper']
    title = top_node['title']
    author = top_node['author']
    abstract = top_node['abstract']
    citation_node = top_node['citations']['citation']
    count = len (citation_node)

    for i in range (count):
        text = citation_node[i]['contexts']
        cit_context.append (text)

    return title, author, abstract, cit_context


def get_info(doi):
    title = None
    abstract = None
    author = None
    citation_contexts = None
    utils.nav_to_data_dir ()
    os.chdir (constants.paper_dir)
    file_name = doi + ".xml"

    if os.path.exists (file_name):
        title, author, abstract, citation_contexts = fetch_all_info_from_xml (file_name)

    os.chdir ("../.")
    utils.nav_to_src ()
    return title, author, abstract, citation_contexts


def search_citations(doi):
    # find Cluster id
    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.doi_clusterId_table
    key_label = 'doi'
    key_contents = doi
    value_label = constants.value_label
    data = dbi.find (table, key_label, key_contents, value_label)
    cluster_id = data[0]

    table = constants.citeGraph_table
    key_label = 'cluster_id'
    key_contents = cluster_id
    value_label = constants.value_label
    citation_list_doi = dbi.find (table, key_label, key_contents, value_label)
    
    url_list = []
    doi_list = []
    for c in citation_list_doi:
        table = constants.clusterId_doi_table
        key = 'cluster_id'
        key_contents = c
        value_label = constants.value_label	
        doi_c = dbi.find (table, key_label, key_contents, value_label)
        if doi_c is not None:
            doi_list.append( doi_c[0])
 
    for doi in doi_list:
        url_list.append (utils.get_url (doi))

    return citation_list_doi, url_list



def write_output(doi,data):
    utils.nav_to_op_dir()
    
    op_file_temp = doi + '_temp.json'
    op_file = doi + '.json'

    json_data = json.dumps (data)
    f = open (op_file_temp, 'w')
    f.write (json_data)
    f.close ()
    os.system(" cat "+ op_file_temp +" | python -m json.tool > " + op_file);
    os.system("rm "+ op_file_temp)
    utils.nav_to_src()
    return

def fetch_data_helper(doi):
    citation_list_doi, citation_list_url = search_citations (doi)
    title, author, abstract, citation_contexts = get_info (doi)
    data = {}
    data['title'] = title
    data['doi'] = doi
    data['author'] = author
    data['abstract'] = abstract
    data['cited_paper_doi'] = citation_list_doi
    data['cited_paper_url'] = citation_list_url
    data['citation_contexts'] = citation_contexts
    op_file = doi + '.json'
    return data

def fetch_data(doi):
    
    # Write to file
    write_output(doi, fetch_data_helper(doi))
    return

    # ------------------------------------------------------------------------------ #
    # Set up and Parse Arguements
    # ------------------------------------------------------------------------------ #


if __name__ == "__main__":
    parser = argparse.ArgumentParser ()
    parser.add_argument ("--doi", help="Comma separated values of doi s for papers [Without SPACE] ")
    parser.add_argument ("--url", help="URL of teh CiteSeer paper , with a doi")
    args = parser.parse_args ()
    doi = args.doi
    url = args.url

    doi_list = []


    if doi is not None:
        doi_list = doi.split (",")

    if url is not None:
        doi_list.append (utils.get_doi_from_url (url))


    for doi in doi_list:
        fetch_data (doi)


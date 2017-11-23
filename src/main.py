import argparse
import constants
import os
import utils
import mongoDBI
import json
from joblib import Parallel, delayed
import random

# open a single connection to speed up things
dbi = mongoDBI.mongoDBI (constants.db_name)
num_parallel = 5
threshold = 15

# Fetch Title, Author, Year
def fetch_base_details(doi):
    # dbi instance to aid concurrency
    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.papers_table
    key_label = constants.paper_key_label
    key_contents = doi
    value_label = constants.value_label
    result = dbi.find (table, key_label, key_contents, value_label)
    if result is None:
        return None, None, None
    try:
        title = result['title']
    except:
        title = None
    try:
        author = result['author']
    except:
        author = None
    try:
        year = result['title']
    except:
        year = None

    return title, author, year


def fetch_abstract_context(doi):
    # dbi instance to aid concurrency
    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.papers_table
    key_label = constants.paper_key_label
    key_contents = doi
    value_label = constants.value_label
    result = dbi.find (table, key_label, key_contents, value_label)

    context_res = None
    abstract_res = None

    if result is None:
        return [abstract_res, context_res]

    if result['abstract'] is not None:
        abstract_res = {doi: result['abstract']}

    if result['citations'] is None or len (result['citations']) == 0:
        context_res = None
    else:
        citation_node = result['citations']
        count = len (citation_node)
        cit_context = []

        for i in range (count):
            try:
                text = citation_node[i]['contexts']
                cit_context.append (text)
            except:
                pass
        context_res = {doi: cit_context}

    return [abstract_res, context_res]


def fetch_all_info_from_db(doi):
    global dbi
    table = constants.papers_table
    key_label = constants.paper_key_label
    key_contents = doi
    value_label = constants.value_label
    result = dbi.find (table, key_label, key_contents, value_label)

    title = result['title']
    author = result['author']
    abstract = {doi: result['abstract']}
    citation_node = result['citations']
    count = len (citation_node)
    cit_context = []

    for i in range (count):
        try:
            text = citation_node[i]['contexts']
            cit_context.append (text)
        except:
            pass

    cit_context_dict = {doi: cit_context}

    return title, author, abstract, cit_context_dict


def search_citations(doi):
    global dbi
    # find Cluster id
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

    if citation_list_doi is None:
        return None

    doi_list = []

    for c in citation_list_doi:
        table = constants.clusterId_doi_table
        key = 'cluster_id'
        key_contents = c
        value_label = constants.value_label
        doi_c = dbi.find (table, key_label, key_contents, value_label)

        if doi_c is not None:
            doi_list.append (doi_c[0])

    return {doi: doi_list}


def write_output(doi, data, file_name=None):
    utils.nav_to_op_dir ()
    op_file_temp = doi + '_temp.json'

    if file_name is None:
        op_file = doi + '.json'
    else:
        op_file = file_name

    json_data = json.dumps (data)
    f = open (op_file_temp, 'w')
    f.write (json_data)
    f.close ()
    os.system (" cat " + op_file_temp + " | python -m json.tool > " + op_file);
    os.system ("rm " + op_file_temp)
    utils.nav_to_src ()
    return


def add_more_data(data, base_doi):
    if base_doi is None:
        return data, []

    base_citation_list_doi = data['cited_paper_doi']
    base_citation_list_url = data['cited_paper_url']
    base_cit_context = data['citation_contexts']
    base_abstract = data['abstract']

    augmented_citation_list_url = []
    augmented_cit_contexts = base_cit_context
    augmented_abstract = base_abstract

    augmented_doi_list = base_citation_list_doi
    augmented_citation_list_url.extend (base_citation_list_url)

    base_doi_list = base_citation_list_doi[base_doi]
    random.shuffle (base_doi_list)

    for b_doi in base_doi_list:

        cit_doi_list = search_citations (b_doi)
        if cit_doi_list is None:
            continue
        for _doi, _doi_list in cit_doi_list.iteritems ():
            augmented_doi_list[_doi] = _doi_list

        list_enriched_cit_urls = enriched_cit_urls (cit_doi_list[b_doi], details=False)
        augmented_citation_list_url.extend (list_enriched_cit_urls)

    # add in the abstracts and contexts

    add_abs_context = Parallel (n_jobs=num_parallel) (delayed (fetch_abstract_context) (doi) for doi in base_doi_list)

    for item in add_abs_context:
        _abs = item[0]
        _context = item[1]

        if type (_abs) is dict:
            for doi_key, _doi_abs in _abs.iteritems ():
                if _doi_abs is None:
                    continue
                augmented_abstract[doi_key] = _doi_abs

        if type (_context) is dict:
            for doi_key, _doi_cxt in _context.iteritems ():
                if _doi_cxt is None:
                    continue
                augmented_cit_contexts[doi_key] = _doi_cxt

    data['abstract'] = augmented_abstract
    data['cited_paper_doi'] = augmented_doi_list
    data['cited_paper_url'] = augmented_citation_list_url
    data['citation_contexts'] = augmented_cit_contexts

    return data, base_doi_list


def create_cit_url_dict(doi, details=False):
    cit_dict = {}
    if details:
        title, author, year = fetch_base_details (doi)
        cit_dict['title'] = title
        cit_dict['author'] = author
        cit_dict['year'] = year
    cit_dict['url'] = utils.get_url (doi)
    return cit_dict


def enriched_cit_urls(doi_list, details=False):
    result = Parallel (n_jobs=num_parallel) (delayed (create_cit_url_dict) (doi, details) for doi in doi_list)
    return result


def fetch_data_helper(doi):
    citation_list_doi = search_citations (doi)
    title, author, abstract, citation_contexts = fetch_all_info_from_db (doi)
    data = {}
    data['title'] = title
    data['doi'] = doi
    data['author'] = author
    data['abstract'] = abstract
    data['cited_paper_doi'] = citation_list_doi
    data['cited_paper_url'] = enriched_cit_urls (citation_list_doi, True)
    data['citation_contexts'] = citation_contexts
    return data


def fetch_data(doi):
    # Write to file
    global threshold
    data = fetch_data_helper (doi)
    data, added_doi = add_more_data (data, doi)

    added_doi_1 = []
    for a_doi in added_doi:
        data, addn_doi  = add_more_data (data, a_doi)
        added_doi_1.append(addn_doi)

    for a_doi in added_doi_1:
        data, _ = add_more_data (data, a_doi)
        if len(data['abstracts']) >= threshold:
            break

    write_output (doi, data)
    return


def fetch_augmented_data(doi):
    data = fetch_data_helper (doi)
    global threshold
    augmented_data, added_doi = add_more_data (data, doi)
    for a_doi in added_doi:
        data, new_dois = add_more_data (data, a_doi)
        if len(data['abstracts']) >= threshold:
            break;
        added_doi.append(new_dois)

    return augmented_data


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


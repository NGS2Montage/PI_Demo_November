import argparse
import constants
import os
import requests



cluster_id_to_doi = {}
def _validate_doi(doi):
    url = constants.csx_paper_url
    url = url.replace ('__DOI__', doi)
    r = requests.get (url)
    return r.status_code == 200

def set_up_cluster_id_to_doi():

    global cluster_id_to_doi
    cwd = os.getcwd ()
    os.chdir (constants.data_dir)
    file_name = constants.clusters_file

    with open (file_name) as f:
        for line in f:
            if ":" in line:
                cur = line.strip (':\n')
                cluster_id_to_doi[ cur ] = [ ]
            else:
                if cur is None: continue
                cur_doi = str (line.strip ('\n'))
                # validate doi and then set cur to None,
                # in case first doi for a cluster is not a valid one
               
                if True or _validate_doi (cur_doi) :
                    cluster_id_to_doi[ cur ].append (cur_doi)
                    cur = None

    os.chdir("../.")
    os.chdir(cwd)
    return

set_up_cluster_id_to_doi()

# --------------------------
# Helper
# --------------------------

def _get_doi_from_clusterid( cluster_id):
    global cluster_id_to_doi
    
    if cluster_id in cluster_id_to_doi.keys():
            return cluster_id_to_doi[ cluster_id ]
    
    return None


def _get_url(doi):
    url = constants.csx_paper_url
    url = url.replace ('__DOI__', doi)
    return url

# --------------------------

# Input :
# List of dois [ a.b.c , d.e.f, ... ]
# Return:
# Cluster id referencing each doi , fetched from clusters.txt
# { doi : cluster_id , .... }

def search_node_id (query_list):
    cur = None
    map = {}

    cwd = os.getcwd ()
    os.chdir (constants.data_dir)
    file_name = constants.clusters_file

    with open (file_name) as f:
        for line in f:
            if ":" in line:
                # a new cluster _id
                cur = line.strip (':\n')
            else:
                if cur == None:
                    continue;
                cur_doi = str (line.strip ('\n'))
                if cur_doi in query_list:
                    map[ cur_doi ] = cur
    # Return back to code directory
    os.chdir ("../.")
    os.chdir (cwd)
    return map


# Input :
# Map  { doi : cluster_id, ...}
# Returns :
# citation dois
# { doi : [ Ciataion_doi ] , ... }

def search_citations(map):
    # node ids have cluster ids
    node_ids = map.values ()
    # cit_map contain :
    # cluster_id : [ cluster ids of citations ]
    cit_map = {}

    for dois in map.values ():
        cit_map[ dois ] = [ ]

    cwd = os.getcwd ()
    os.chdir (constants.data_dir)
    file_name = constants.graph_file
    cur_id = None

    with open (file_name) as f:
        for line in f:
            if ":" in line:
                cur_id = line.strip (':\n')
            else:
                if cur_id is None:
                    continue;
                if cur_id in node_ids:
                    z = str (line.strip ('\n'))
                    # place the cluster id ( corr to doi ) in the map  ; [cur_id] : < cluster_id >
                    if cur_id in cit_map.keys ():
                        cit_map[ cur_id ].append (z)
                    else:
                        cit_map[ cur_id ] = [ z ]

    # Return back to code directory
    os.chdir ("../.")
    os.chdir (cwd)

    inv_map = {v: k for k, v in map.iteritems ()}

    # Place doi in place of config _id
    cit_doi_map = {}
    for key,value in cit_map.iteritems():
        cur_doi = inv_map[key]
        if cur_doi is None : continue

        cit_doi_map[ cur_doi ] = []
        for v in value:
            v_doi = _get_doi_from_clusterid(v)
            if v_doi is not None :
                cit_doi_map[cur_doi].append(v_doi[0])
    return cit_doi_map;



# ------------------------------------------------------------------------------ #
# Set up and Parse Arguements
# ------------------------------------------------------------------------------ #


parser = argparse.ArgumentParser ()
parser.add_argument ("--doi", help="Comma separated values of doi s for papers [Without SPACE] ")
args = parser.parse_args ()
doi = args.doi
doi_list = doi.split (",")
map = search_node_id (doi_list)
cit_doi_map = search_citations (map)

# get URL from dois
for key,value in cit_doi_map.iteritems():
    print('----')
    print key
    for v in value:
        print _get_url(v)
    print('-----')
#End#

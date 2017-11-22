import constants
import mongoDBI
import utils
import os
import setup_data


#
# ingest cluster_id -- > [ doi ] from ccitegraph.txt
#

def ingest_clusterId_doi():
    utils.nav_to_data_dir ()
    cluster_id_to_doi = {}
    doi_clusterId = {}
    file_name = constants.clusters_file

    with open (file_name) as f:
        for line in f:
            if ":" in line:
                cur_cluster_id = line.strip (':\n')
                cluster_id_to_doi[ cur_cluster_id ] = [ ]
            else:
                if cur_cluster_id is None: continue
                cur_doi = str (line.strip ('\n'))

                if constants.validate_ingest_url and not utils.validate_doi (cur_doi):
                    continue;

                cluster_id_to_doi[ cur_cluster_id ].append (cur_doi)

                if cur_doi not in doi_clusterId:
                    doi_clusterId[ cur_doi ] = [ ]
                doi_clusterId[ cur_doi ].append (cur_cluster_id)

    # Write clusterId -> list[ doi ]
    # doi_clusterId
    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.clusterId_doi_table
    data_map = {}
    data_map[ table ] = [ ]
    for cluster_id, doi_list in cluster_id_to_doi.iteritems ():
        key_label = 'cluster_id'
        key_contents = cluster_id
        value_label = constants.value_label
        value_contents = doi_list

        element = dbi.get_insert_dict (key_label, key_contents, value_label, value_contents)
        data_map[ table ].append (element)
    dbi.insert_bulk (data_map)

    # Write doi -> list[cluster ID]
    # doi_clusterId

    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.doi_clusterId_table
    data_map = {}
    data_map[ table ] = [ ]
    for doi, clusterId_list in doi_clusterId.iteritems ():
        key_label = 'doi'
        key_contents = doi
        value_label = constants.value_label
        value_contents = clusterId_list

        element = dbi.get_insert_dict (key_label, key_contents, value_label, value_contents)
        data_map[ table ].append (element)
    dbi.insert_bulk (data_map)

    utils.nav_to_src ()
    return;

#
# ingest cluster_id -- > [ cluster ids cited by it ] from ccitegraph.txt
#

def ingest_citegraph():
    utils.nav_to_data_dir ()
    citegraph_map = {}
    file_name = constants.graph_file
    cur_cluster_id = None
    with open (file_name) as f:
        for line in f:
            if ":" in line:
                cur_cluster_id = line.strip (':\n')
                citegraph_map[ cur_cluster_id ] = [ ]
            else:
                if cur_cluster_id is None: continue
                cur_doi = str (line.strip ('\n'))
                citegraph_map[ cur_cluster_id ].append (cur_doi)

    dbi = mongoDBI.mongoDBI (constants.db_name)
    table = constants.citeGraph_table

    data_map = {}
    data_map[table] = [ ]

    for cluster_id, cluster_list in citegraph_map.iteritems ():

        key_label = 'cluster_id'
        key_contents = cluster_id
        value_label = constants.value_label
        value_contents = cluster_list	
        element = dbi.get_insert_dict (key_label, key_contents, value_label, value_contents)
        data_map[ table ].append (element)
    
    dbi.insert_bulk (data_map)
    utils.nav_to_src ()
    return;


setup_data.init_checks()
ingest_clusterId_doi()
ingest_citegraph ()


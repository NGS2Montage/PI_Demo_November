import os
import sys
import os.path
import constants
import shutil


#########################3

def download_files():
    tmp_dir = "tmp"
    try:
        shutil.rmtree (tmp_dir)
    except:
        pass

    os.makedirs (tmp_dir)
    os.chdir (tmp_dir)

    file1_url = "https://www.dropbox.com/s/ck8zxfb7resc9ze/CSXCitegraph-2014-01-13.tar.gz?dl=0"
    op2 = "CSXCitegraph.tar.gz"
    dir = "CSXCitegraph"
    os.system ("wget " + file1_url + " -O " + op2)
    os.system ("tar xvf " + op2 )
    os.system (" cp -r " + dir + "/" + constants.graph_file + " ../.")

    file1_url = "https://www.dropbox.com/s/ybv5t7sc2ql76yb/k0.7j-nsw-3g-t-citeseerx-pub.tar.gz?dl=0"
    op1 = "papers_data.tar.gz"
    dir = "papers_data"
    os.system ("wget " + file1_url + " -O " + op1)
    os.system ("tar xvf " + op1 + " -C " + dir)
    os.system (" mv k0.7j-nsw-3g-t-citeseerx-pub/papers"  + "  ../." )

    file1_url = "https://www.dropbox.com/s/9w9bkpe6mu5t6of/CSXClusters-2014-01-13.tar.gz?dl=0"
    op3 = "CSXClusters.tar.gz"
    dir = "CSXClusters"
    os.system ("wget " + file1_url + " -O " + op3)
    os.system ("tar xvf " + op3 )
    os.system (" cp -r " + dir + "/" + constants.clusters_file + " ../.")

    os.chdir ("../.")
    try:
        shutil.rmtree (tmp_dir)
    except:
        pass
    return


def init_checks():
    cwd = os.getcwd ()
    file_path = constants.data_dir_location
    os.chdir (file_path)

    if not os.path.exists (constants.data_dir):
        os.makedirs (constants.data_dir)

    os.chdir (constants.data_dir)

    # files are not presen, Download them
    if not os.path.exists (constants.graph_file) or not os.path.exists (constants.clusters_file) or True:
        download_files ()

    os.chdir (cwd)
    return

# PI_Demo_November

Source Data
------


CiteSeer dataset
https://www.dropbox.com/s/ybv5t7sc2ql76yb/k0.7j-nsw-3g-t-citeseerx-pub.tar.gz?dl=0

Citation graph:
https://www.dropbox.com/s/ck8zxfb7resc9ze/CSXCitegraph-2014-01-13.tar.gz?dl=0

The clusters and the corresponding DOIs:
https://www.dropbox.com/s/9w9bkpe6mu5t6of/CSXClusters-2014-01-13.tar.gz?dl=0

[ wget <link> and tar -xvf <filename> ]


------



For Initial setup + ingestion :
python ingest.py

For just downloading the data ( recommended on server, since dat on db already set up)

Call setup_data.py - init_checks() 

-------

Ensure directory structure :
src
data_dir
output
( setup_data takes care of it )

-------

To get the output :

src/main.py --url

src/main.py --doi

For help , src/main.py -h

Then check:          output/<doi>.json

-------

Example :

python main.py --url http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.2545

python main.py --doi 10.1.1.61.2545



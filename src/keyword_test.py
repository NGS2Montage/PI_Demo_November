from pathlib import Path
import os
import json
import spacy
from collections import OrderedDict

import pprint




# Clean text
def clean_text(text):
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load('en')
    # Process a document, of any size
    doc = nlp(text)

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)

    return doc

def access_feature(feat_name, feat):

    if bool(feat):
        if feat_name == 'abstract':
            if bool(feat):  # Non-empty abstract
                return feat
            else:
                return None
        else:
            flag = False
            print(feat)
            txt_str = u''
            # Check if this list is empty or not
            for i in range(len(feat)):
                if bool(feat[i]):
                    flag = True
                    txt_str = txt_str + feat[i]

            if flag:  # It is empty, return None
                print(txt_str)
                return txt_str
            else:
                return None
    else:
        return None

parent_dir = str(Path().resolve().parent)
source_path = os.path.join(parent_dir, 'output')

# Read the files in the outpur dictionary
f = []
for (dirpath, dirnames, filenames) in os.walk(source_path):
    f.extend(filenames)

ref_paper = '10.1.1.30.6583.json'

paper_keys = []
cited_data = OrderedDict()
needed_feat = ['abstract', 'citation_contexts']
# [u'doi', u'author', u'abstract', u'title', u'citation_contexts', u'cited_paper_doi', u'cited_paper_url']

for file_name in filenames:
    # Reading data from the other file
    filepath = os.path.join(source_path, file_name)
    with open(filepath) as json_file:
        data = json.load(json_file)
    json_file.close()  # close the file

    if not paper_keys:
        paper_keys = data.keys()

    txt_str = u''
    str1 = access_feature('abstract', data['abstract'])
    str2 = access_feature('citation_contexts', data['citation_contexts'])

    if bool(str1) or bool(str2):

        if bool(str1):
            txt_str = txt_str + str1
            print str1

        if bool(str2):
            txt_str = txt_str + str2
            print str2

        cited_data[data['doi']] = txt_str

for key in cited_data.keys():

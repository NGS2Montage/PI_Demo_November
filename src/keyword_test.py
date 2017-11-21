from pathlib import Path
import os
import json
from collections import OrderedDict
import clean_text_manual as ctm

# Set up spaCy
from spacy.lang.en import English

# Setup nltk and other preprocessor
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt') # if necessary...

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    '''remove punctuation, lowercase, stem'''
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


# Parse text using spacy
def parse_text_spacy(text):
    # Load English tokenizer, tagger, parser, NER and word vectors
    parser = English()
    # Process a document, of any size
    parsedData = parser(text)



    print '\n\n\n'
    '''
    # Find named entities, phrases and concepts
    for entity in parsedData.ents:
        print(entity.text, entity.label_)

    # Let's look at the tokens
    # All you have to do is iterate through the parsedData
    # Each token is an object with lots of different properties
    # A property with an underscore at the end returns the string representation
    # while a property without the underscore returns an index (int) into spaCy's vocabulary
    # The probability estimate is based on counts from a 3 billion word
    # corpus, smoothed using the Simple Good-Turing method.
    for i, token in enumerate(parsedData):
        print("original:", token.orth, token.orth_)
        print("lowercased:", token.lower, token.lower_)
        print("lemma:", token.lemma, token.lemma_)
        print("shape:", token.shape, token.shape_)
        print("prefix:", token.prefix, token.prefix_)
        print("suffix:", token.suffix, token.suffix_)
        print("log probability:", token.prob)
        print("Brown cluster id:", token.cluster)
        print("----------------------------------------")
    '''

    return parsedData


def access_feature(feat_name, feat):

    if bool(feat):
        if feat_name == 'abstract':
            if bool(feat):  # Non-empty abstract
                return feat
            else:
                return None
        else:
            flag = False
            txt_str = u''
            # Check if this list is empty or not
            for i in range(len(feat)):
                if bool(feat[i]):
                    flag = True
                    txt_str = txt_str + feat[i]

            if flag:  # It is empty, return None
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

    # Filtering the corrupt files to get the abstract and context (if exists)
    txt_str = u''
    str1 = access_feature('abstract', data['abstract'])
    str2 = access_feature('citation_contexts', data['citation_contexts'])

    # Aggregate the abstract and the citation_contexts into one string (either should exist)
    if bool(str1) or bool(str2):

        if bool(str1):
            txt_str = txt_str + str1

        if bool(str2):
            txt_str = txt_str + u' ' + str2

        '''
        parsedText = parse_text_spacy(txt_str)  # Parse the aggregated text via spacy parser

        # Aggregate the parsed text into a string
        txt_str = ''
        for entity in parsedText:
            txt_str = txt_str + str(entity)
            txt_str = txt_str + ' '
        '''
        if file_name == ref_paper:
            ref_doc = txt_str
        else:
            cited_data[data['doi']] = txt_str
        '''

        # Manual package written by me
        if file_name == ref_paper:
            ref_doc = ctm.text_to_clean(txt_str)
        else:
            cited_data[data['doi']] = ctm.text_to_clean(txt_str)
        '''

similarity_score = OrderedDict()

'''
# Find the similarity of the reference document with the other documents
for key in cited_data.keys():
    similarity_score[key] = ref_doc.similarity(cited_data[key])
    print key, similarity_score[key]
'''
print ref_doc, '\n\n'
# Find the cosine similarity of the documents
for key in cited_data.keys():
    similarity_score[key] = cosine_sim(ref_doc, cited_data[key])
    print key, similarity_score[key]



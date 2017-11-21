import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings")

import django
django.setup()

from redlev.models import ThresholdSamples
import pandas as pd
import numpy as np

from scipy import interpolate
from scipy.stats import norm

dir_path = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(dir_path,'plotData.txt')

def get_numeric(x):
    string = x.split('[')[-1].split(']')[0].split(', ')
    return max([float(x) for x in string])

data = pd.read_csv(data_file, index_col=0)
data['max_val'] = data['dist'].apply(lambda x: get_numeric(x))
data = data[data['max_val'] > 0]
data = data.reset_index(drop=True)
data.rename(columns={'actRng':'activeRange'}, inplace=True)

for key, val in data.iterrows():
    newRow = ThresholdSamples.objects.update_or_create(**val)
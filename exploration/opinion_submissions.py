import os
from pathlib import Path
from collections import Counter

import pickle
import numpy as np

import pandas as pd
from tqdm import tqdm
tqdm.pandas()

from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

import warnings
warnings.simplefilter("ignore", UserWarning)


# Data directory
DATA_DIR = Path(os.getcwd()).parent / 'data'

submissions = pd.read_json(DATA_DIR / 'reddit_submissions.json.bz2')

pkl_filename = '/work3/s194253/RandomForest_TwitterOpinion500_iter.pkl'

with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

submissions['text'] = submissions['title'] + " " + submissions['selftext']

# load stop-words
stop_words = set(stopwords.words('english'))

# add webpages to stopwords
stop_words.add('http') 
stop_words.add('https')

# Preprocess the text 
porter = PorterStemmer()
exclusions = {'RT'}

# define tokenizing function
clean = lambda x: Counter([porter.stem(word_token).lower() for word_token in word_tokenize(x) \
                       if word_token.lower() not in stop_words \
                       and word_token.isalpha() \
                       and word_token not in exclusions])

# apply tokenizing to texts - progress_apply for seeing progress bar WHEN running
tokens = []
for i, text in enumerate(tqdm(submissions['text'])):
    try:
        text_tokens = clean(text)
        tokens.append(text_tokens)
    except TypeError:
        tokens.append([''])

#tokens = submissions['text'].progress_apply(lambda text: clean(text))
submissions['tokens'] = tokens

# join tokens to one string
submissions['processed_text'] = submissions['tokens'].progress_apply(lambda x: ' '.join(str(v) for v in x))


submissions['year'] = submissions.date.progress_apply(lambda x: x.year)
submissions.year.unique()

for year in submissions.year.unique():
    sub_submissions = submissions[submissions.year == year]
    X = sub_submissions['processed_text'].to_numpy()
    opinions = ['NaN'] * X.__len__()
    probs = ['NaN'] * X.__len__()

    print(year)
    for i, x in enumerate(tqdm(X)):
        pred = model.predict([x])
        opinions[i] = pred[0]
        probs[i] = model.predict_proba([x])[0]

    sub_submissions['opinion'] = opinions
    sub_submissions['opinion_probs'] = probs

    sub_submissions.to_json(f'/work3/s194253/submissions_opinion_{year}.json.bz2')

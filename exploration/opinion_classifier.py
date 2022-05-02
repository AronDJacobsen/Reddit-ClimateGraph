from pathlib import Path
import time
import os, sys

import numpy as np
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV

from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score, balanced_accuracy_score

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Data load
DATA_DIR = Path(os.getcwd()).parent / 'data'

filename = 'twitter_sentiment_data.csv'
tweets = pd.read_csv(DATA_DIR/filename)

class_mapping = {2: 'News',
                 1: 'Pro',
                 0: 'Neutral',
                 -1: 'Anti'}

tweets['label'] = tweets['sentiment'].progress_apply(lambda x: class_mapping[x])

# define smallest group
smallest_group = tweets[tweets['label'] == 'Anti']
smallest_group_size = smallest_group.__len__()

# downsample each class to the size of the smallest group
temp = [smallest_group]
for label in class_mapping.values():
    if label != 'Anti':
        temp.append(tweets[tweets['label'] == label].sample(smallest_group_size, random_state=42))
        
# create balanced dataset
tweets_balanced = pd.concat(temp)

# shuffle and reindex the data
tweets_balanced = tweets_balanced.sample(frac=1, random_state=42)
tweets_balanced = tweets_balanced.reset_index().drop('index', axis=1)


# load stop-words
stop_words = set(stopwords.words('english'))

# add webpages to stopwords
stop_words.add('http') 
stop_words.add('https')

porter = PorterStemmer()

#TODO: REVISIT THIS maybe

exclusions = {'RT'}

# define tokenizing function
clean = lambda x: set([porter.stem(word_token).lower() for word_token in word_tokenize(x) \
                       if word_token.lower() not in stop_words \
                       and word_token.isalpha() \
                       and word_token not in exclusions])

# apply tokenizing to texts - progress_apply for seeing progress bar WHEN running
tokens = tweets_balanced['message'].progress_apply(lambda text: clean(text))
tweets_balanced['tokens'] = tokens

tweets_balanced['processed_message'] = tweets_balanced['tokens'].progress_apply(lambda x: (" ").join(x))

print("Creating numpy...", file=sys.stderr)
tweets_balanced['processed_message'].to_numpy()


X = tweets_balanced['processed_message'].to_numpy()
y = tweets_balanced['label'].to_numpy()

print("Splitting data...", file=sys.stderr)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("Classification object...", file=sys.stderr)
text_clf = text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', RandomForestClassifier(criterion='gini', random_state=42))
])

# Create the random grid
parameters = {'clf__n_estimators': [800, 1000, 1200, 1400, 1600, 1800, 2000],
               'clf__max_features': ['sqrt', 'auto'],
               'clf__max_depth': [90, 100, 110, 120, 130, 140],
               'clf__min_samples_split': [2, 4, 6, 8, 10],
               'clf__min_samples_leaf': [1, 2, 3, 4],
               'clf__bootstrap': [False, True]}

print("Running optimization...", file=sys.stderr)
rs_clf = RandomizedSearchCV(text_clf, parameters, n_iter=500, cv=5, verbose=3)
rs_clf = rs_clf.fit(X_train, y_train)

print(rs_clf.best_score_)
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, rs_clf.best_params_[param_name]))

import pickle
model = rs_clf

pkl_filename = '/work3/s194253/RandomForest_TwitterOpinion500_iter.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)



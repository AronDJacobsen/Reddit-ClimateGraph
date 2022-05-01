import os
from pathlib import Path
import time, datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

from psaw import PushshiftAPI
import networkx as nx

import warnings
warnings.simplefilter("ignore", UserWarning)

api = PushshiftAPI()

# define search conditions
queries = ['climate change  climate',
           'global warming  climate',
           'warming planet  climate']
 
# define time interval
start_date = int(datetime.datetime(2014, 11, 1).timestamp())
end_date = int(datetime.datetime(2022, 4, 5).timestamp())

# parameters to modify extend of data retrieval
limit = 250
num_intervals = 10848 #4001

def select_attributes(attributes, results):
    temp = []
    for my_submission in results:
        temp_dict = {}
        for att in attributes:
            try:
                temp_dict[att] = my_submission.d_[att]
            except KeyError:
                temp_dict[att] = np.nan
        temp.append(temp_dict)
    return temp


# specify attributes of interest
attributes = ['id', 'author', 'title', 'selftext', 'score', 'created_utc', 'subreddit', 'num_comments', 'all_awardings', 'awarders', 'total_awards_received']
df_submissions = pd.DataFrame()

# search API for submissions
date_linspace = np.linspace(start_date, end_date, num_intervals, dtype=np.int64)

for i in tqdm(range(1, date_linspace.__len__())):
    # define parameters
    date1 = date_linspace[i-1]
    date2 = date_linspace[i]
    results = []

    # query all queries
    for j, query in enumerate(queries):
        gen = api.search_submissions(after=date1,
                                     before=date2,
                                     q=query,
                                     limit=limit)
        temp_results = list(gen)
        results += temp_results
        
        if temp_results.__len__() == limit:
            print(f"Limit exceeded at index {i, j}")
    
    # create structure for dataframe (nested loop because 2014 data does not have awards)
    sub4df = select_attributes(attributes, results)
    
    # create dataframe continuously
    temp_df = pd.DataFrame.from_dict(sub4df)
    df_submissions = pd.concat([df_submissions, temp_df])
    
    # drop the duplicated ids
    df_submissions = df_submissions.drop_duplicates('id', keep='first')

# reset index    
df_submissions = df_submissions.reset_index(drop=True)

print(f"Are all duplicates removed? {df_submissions.id.is_unique}")

# modify dataframe
df_submissions['date'] = df_submissions['created_utc'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).date())
df_submissions = df_submissions.drop('created_utc', axis=1)

print(f"Shape of dataframe: {df_submissions.shape}")
df_submissions.head()

# save dataframe as a pickle
path = Path(os.getcwd()).parent
df_submissions.to_pickle(path / 'data/reddit_submissions.bz2')


# search API for comments
results = []
limit = 25 

for i, submission in tqdm(df_submissions.iterrows(), total=df_submissions.__len__()):
    gen = api.search_comments(subreddit=submission.subreddit,
                              link_id=submission.id, 
                              size=limit)
    temp_results = list(gen)
    results += temp_results
    
    if temp_results.__len__() == limit:
        print(f"Limit exceeded at index {idx}")

# specify attributes of interest
attributes = ['id', 'link_id', 'score', 'created_utc', 'author', 'parent_id', 'body', 'controversiality', 'total_awards_received', 'all_awardings', 'associated_award']

# create dataframe
sub4df = select_attributes(attributes, results)
df_comments = pd.DataFrame.from_dict(sub4df)

# modify dataframe
df_comments.rename(columns={'link_id':'submission_id', 'body':'text'}, inplace=True)
df_comments['date'] = df_comments['created_utc'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).date())
df_comments = df_comments.drop('created_utc', axis=1)

print(f"Shape of dataframe: {df_comments.shape}")
df_comments.head()

# save dataframe as a pickle
path = Path(os.getcwd()).parent
df_comments.to_pickle(path / 'data/reddit_comments.bz2')
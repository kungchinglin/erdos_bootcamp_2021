#!/usr/bin/env python3
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
words_to_keep = ['above','all', 'below', 'further', 'until', 'under']
for word in words_to_keep:
    STOPWORDS.remove(word)

import praw
reddit = praw.Reddit(
    client_id="kxbUr-4PyE7DlQ",
    client_secret="Q5rIAPS9IHZ1QgOIkHNY09Y9VMxDsA",
    password="AACAXZDE",
    user_agent="testscript by u/kc_the_scraper",
    username="kc_the_scraper",
)


import pickle
## Load the model and vectorizer
with open("vectorizer.pkl", 'rb') as fvec:
    vect = pickle.load(fvec)
with open("model_test.pkl", 'rb') as fmod:
    saved_model = pickle.load(fmod)


def prepare_text(text):
    if not text:
        return ""
    text = text.lower()
    # remove \n
    text = re.sub("\\n", " ", text)
    # remove 've, 're
    text = re.sub("[a-z]*\'[r,v]e", "", text)
    # remove 's, 't, 'r, 'v
    text = re.sub("[a-z]*\'[s,t,r,v]", "", text) 
    # Replace everything not a letter with a space
    text = re.sub("[^a-zA-Z]", " ", text)
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    return text

def add_processed_columns(df):
    # process body, title and author name
    df['body_processed'] = df['body'].apply(prepare_text)
    df['title_processed'] = df['title'].apply(prepare_text)
    df['author_processed'] = df['author'].apply(prepare_text)
    # combine the features
    df['body_and_title'] = df['body_processed']+' '+df['title_processed']
    df['body_and_author'] = df['body_processed']+' '+df['author_processed']
    df['title_and_author'] = df['title_processed']+' '+df['author_processed']
    df['body_title_and_author'] = df['body_processed']+' '+df['title_processed']+' '+df['author_processed']
    return df

def get_reddit_info(url):
    Sub = reddit.submission(url = url)
    data={'score':[Sub.score],
              'body':[Sub.selftext],
              'created_utc': [Sub.created_utc],
              'ext_link': [Sub.url],
              'title':[Sub.title],
              'subreddit':[Sub.subreddit.display_name],
              'upvote_ratio':[Sub.upvote_ratio],
              'author':[Sub.author.name],
              'original_url':[url]}
    return pd.DataFrame(data, index=None)

def process_data(input_url, xcol="body_and_title"):
    df = get_reddit_info(input_url)
    df = add_processed_columns(df)
    X_tfidf = vect.transform(df[xcol].values)
    #df = prepare_score_label(df, ycol='score', threshold=1000)
    return X_tfidf

def predict(X):
    return saved_model.predict(X)[0]

def make_prediction(url):
    X_input= process_data(url)
    pred = predict(X_input)
    return pred

if __name__=="__main__":
    in1 = "https://www.reddit.com/r/postsreddit/comments/jjuci1/do_people_engage_more_when_you_post_an_earnest/"
    pred = make_prediction(in1)
    print (pred)


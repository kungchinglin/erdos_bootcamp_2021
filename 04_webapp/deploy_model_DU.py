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
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='')


import pickle

import joblib

def get_reddit_info(url):
    Sub = reddit.submission(url = url)
    df = {'score': Sub.score,
              'body': Sub.selftext,
              'created': Sub.created_utc,
              'ext_link': Sub.url,
              'title': Sub.title,
              'subreddit': Sub.subreddit.display_name,
              'upvote_ratio': Sub.upvote_ratio,
              'author': Sub.author.name,
              'original_url': url}
    return df

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
    # process body, title, author name, and subreddit forum
    df['body_processed'] = prepare_text(df['body'])
    df['title_processed'] = prepare_text(df['title'])
    df['author_processed'] = prepare_text(df['author'])
    # combine the features
    df['body_title_author_subreddit'] = df['body_processed']+ ' ' + \
                                        df['title_processed']+ ' ' + \
                                        df['author_processed']+ ' ' + \
                                        df['subreddit']
    return df

# Sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(inp, sent):
    return analyzer.polarity_scores(str(inp))[sent]

def sent2words(sent, sent_mean, prefix):
    if sent < sent_mean:
        out = prefix + '_low'
    else:
        out = prefix + '_high'
    return out

def to_hour(inp):
    return int(round(inp.hour + (inp.minute/60.) + (inp.second/3600.)))

from num2words import num2words
import re

def get_num2words(num, prefix):
    w = num2words(num)
    w = re.sub(' ', '_', w)
    w = re.sub('-', '_', w)
    return prefix + '_' + w

# External link
image_file_formats = ['ai','bmp','gif','ico','jpg','jpeg','png','ps','psd','svg','tif','tiff']
video_file_formats = ['.3g2','3gp','avi','flv','h264','m4v','mkv','mov','mp4','mpg','mpeg','rm','swf','vob','wmv']

def get_ext_media(inp):
    if (inp == None) or (inp == 0):
        last_term = 'None'
    else:
        last_term = str(inp).split('.')[-1]

    if last_term in image_file_formats:
        out = 'has_image'
    elif last_term in video_file_formats:
        out = 'has_video'
    elif last_term == 'None':
        out = 'no_ext_link'
    else:
        out = 'just_web'
    return out


# Other text attributes
import string
import re

def emoji_count(s):
    s = ''.join(word.strip(string.punctuation) for word in str(s).split())
    return len(re.findall('[^\w\s,\(\)\'\/-]',s))

def countUpper(text):
    Up = 0
    Low = 0
    for ch in str(text):
        if ch.isupper():
            Up += 1
        elif ch.islower():
            Low += 1

    if Up + Low:
        return Up
    else:
        return 0

def exclamationAndQuestion(text):
    return str(text).count('!') + str(text).count('?')

#------------------------------

def data_processing(input_url):

    # Text processing
    df = get_reddit_info(input_url)
    df = add_processed_columns(df)

    # Sentiment analysis
    for sent in ['pos', 'neg', 'neu', 'compound']:
        df[sent+'_sent'] = analyzer.polarity_scores(str(df['title_processed']))[sent]
    for col in ['pos_sent','neg_sent','neu_sent','compound_sent']:
        df[col] = sent2words(df[col], sent_mean=0.5, prefix=col)

    # Transforming time info
    df['posting_time'] = dt.datetime.fromtimestamp(df['created'])
    df['posting_year'] = df['posting_time'].year
    df['posting_month'] = df['posting_time'].month
    df['posting_date'] = df['posting_time'].day
    df['posting_day'] = df['posting_time'].weekday()
    df['posting_hour'] = to_hour(df['posting_time'])

    # External media
    df['ext_link_media'] = get_ext_media(df['ext_link'])

    # Length of text
    df['title_length'] = len(str(df['title_processed']).split())
    df['body_length']  = len(str(df['body_processed']).split())

    # Text properties
    df['title_emoji'] = emoji_count(df['title'])
    df['body_emoji']  = emoji_count(df['body'])
    df['title_EQ']    = exclamationAndQuestion(df['title'])
    df['body_EQ']     = exclamationAndQuestion(df['body'])
    df['title_UL']    = countUpper(df['title'])
    df['body_UL']     = countUpper(df['body'])

    # Turning numerics to words
    cols = ['posting_date','posting_day','posting_hour','title_length','body_length',
            'title_emoji','body_emoji','title_EQ','body_EQ','title_UL','body_UL']
    for col in cols:
        df[col] = get_num2words(df[col], prefix=col)

    return df


# Combining all features and transform to TFIDF
def text2tfidf(df):
    features = ['body_title_author_subreddit', 'pos_sent', 'neg_sent',
                'neu_sent', 'compound_sent', 'posting_date', 'posting_hour', 'posting_day',
                'ext_link_media', 'title_length', 'body_length', 'title_emoji',
                'body_emoji', 'title_EQ', 'body_EQ', 'title_UL', 'body_UL']

    all_text = ''
    for feat in features:
        all_text += ' ' + df[feat]

    return vect.transform([all_text])

def predict(tfidf, saved_model, thresh):
    prob = saved_model.predict_proba(tfidf)[0][1]
    if prob > thresh:
        pred = 1
    else:
        pred = 0
    return pred

# -------------------------

if __name__ == '__main__':

    # User input
    input_url = "https://www.reddit.com/r/postsreddit/comments/jjuci1/do_people_engage_more_when_you_post_an_earnest/"
    input_recall = 0.2

    # Upload vectorizer
    with open("tfidf_vectorizer_DU.pkl", 'rb') as fvec:
        vect = pickle.load(fvec)

    # Upload model
    model = 'xgboost_tfidf_depth_3.joblib'
    saved_model = joblib.load(model)

    # Upload recall list
    with open("recall.pkl", 'rb') as rec:
        recall_list = pickle.load(rec)

    # Determining threshold based on user input
    thresh = np.interp(input_recall, recall_list[::-1], np.arange(0.01,1.0,0.01)[::-1])

    df = data_processing(input_url)
    tfidf = text2tfidf(df)
    pred = predict(tfidf, saved_model, thresh)

    print(pred)

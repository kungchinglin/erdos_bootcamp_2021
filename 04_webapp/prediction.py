#!/usr/bin/env python3
import numpy as np
import re

# load STOPWORDS 
sw = open('english_STOPWORDS', 'r')
#STOPWORDS = set(sw.readlines())
STOPWORDS = set([w.strip("\n") for w in sw.readlines()])

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

def add_processed_data(data):
    # process body, title and author name
    data['body_processed'] = prepare_text(data['body'])
    data['title_processed'] = prepare_text(data['title'])
    data['author_processed'] = prepare_text(data['author'])

    # combine the features
    data['body_and_title'] = data['body_processed']+' '+data['title_processed']
    data['body_and_author'] = data['body_processed']+' '+data['author_processed']
    data['title_and_author'] = data['title_processed']+' '+data['author_processed']
    data['body_title_and_author'] = data['body_processed']+' '+data['title_processed']+' '+data['author_processed']
    return data

def get_reddit_info(url):
    Sub = reddit.submission(url = url)
    data={'score':Sub.score,
              'body':Sub.selftext,
              'created_utc': Sub.created_utc,
              'ext_link': Sub.url,
              'title':Sub.title,
              'subreddit':Sub.subreddit.display_name,
              'upvote_ratio':Sub.upvote_ratio,
              'author':Sub.author.name,
              'original_url':url}
    return data 

def process_data(input_url, vect, xcol="body_and_title"):
    data_from_reddit = get_reddit_info(input_url)
    data_processed = add_processed_data(data_from_reddit)
    X_tfidf = vect.transform([data_processed[xcol]])
    return X_tfidf

def predict(X, model):
    return model.predict(X)[0]

def make_prediction(url, vectorizer, model, strategy="Aggressive"):
    X_input= process_data(url, vectorizer)
    pred = predict(X_input, model)
    return pred

if __name__=="__main__":
    input_url = "https://www.reddit.com/r/postsreddit/comments/jjuci1/do_people_engage_more_when_you_post_an_earnest/"
    pred = make_prediction(input_url)
    print (pred)


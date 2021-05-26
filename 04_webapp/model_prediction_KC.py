#!/usr/bin/env python3
import numpy as np
import pandas as pd
import re
import datetime as dt

import praw
import pickle
import string

def emoji_count(s):
    s = ''.join(word.strip(string.punctuation) for word in s.split())
    return len(re.findall('[^\w\s,\(\)\'\/-]',s))

def hourOfDay(utc):
    return dt.datetime.utcfromtimestamp(utc).hour

def dayOfWeek(utc):
    return dt.datetime.utcfromtimestamp(utc).weekday()

def textLength(text):
    return len(text.split())

def postType(link):
    if not link:
        return 'others'
    if 'png' in link or 'jpg' in link:
        return 'figures'
    elif '/r/' in link:
        return 'others'
    else:
        return 'outside_link'

def countUpper(text):
    Up = 0
    Low = 0
    for ch in text:
        if ch.isupper():
            Up += 1
        elif ch.islower():
            Low += 1
    
    if Up + Low:
        return Up/(Up+Low)
    else:
        return 0
    
def exclamationAndQuestion(text):
    return text.count('!') + text.count('?')

def getMonth(utc):
    return dt.datetime.utcfromtimestamp(utc).month

def getPushShiftDataAuthor(after,before, sub, author):
    ids = []
    while after < before:
        params = '&after='+str(int(after))+'&before='+str(int(before))+'&subreddit='+str(sub)+'&author='+str(author)
        url = 'https://api.pushshift.io/reddit/search/submission/?size=100' + params
        r = requests.get(url)
        data = json.loads(r.text)['data']
       
        ids += list(map(lambda x: x['id'], data))
        after = data[-1]['created_utc'] + 1
        if len(data) < 100:
            break 
    return ids


def getPostHistory(ids, upperLimit):

    if not ids:
        return 0, 1
    
    totalScore = 0
    
    limit = min(len(ids), upperLimit)
    
    ids = ids[:limit]
    
    for ID in ids:
        Sub = reddit.submission(id = ID)
        totalScore += Sub.score
    
    return limit, totalScore/limit

def getAuthorFeatures(after, submissionTime, sub, author, upperLimit = 50):
    ids = getPushShiftDataAuthor(after, submissionTime - 1, sub, author)
    
    return getPostHistory(ids, upperLimit)
    
def primeTime(hour):
    primeTime = 1 if hour >= 7 and hour <= 11 else 0
    
    return primeTime

def weekend(day):
    return 1 if day >= 5 else 0

def featureProcessing(df_model):

    df_model['title_emoji'] = df_model['title'].apply(emoji_count)
    df_model['body_emoji'] = df_model['body'].apply(emoji_count)
    df_model['title_length'] = df_model['title'].apply(textLength)
    df_model['body_length'] = df_model['body'].apply(textLength)
    df_model['title_EQ'] = df_model['title'].apply(exclamationAndQuestion)
    df_model['body_EQ'] = df_model['body'].apply(exclamationAndQuestion)
    df_model['title_UL'] = df_model['title'].apply(countUpper)
    df_model['body_UL'] = df_model['body'].apply(countUpper)    
    df_model['hour'] = df_model['created'].apply(hourOfDay)
    df_model['day'] = df_model['created'].apply(dayOfWeek)
    df_model['post_type'] = df_model['ext_link'].apply(postType)
    df_model['prime_time'] = df_model['hour'].apply(primeTime)
    df_model['weekend'] = df_model['day'].apply(weekend)
    df_model['month'] = df_model['created'].apply(getMonth)

    df_model['figures'] = 1 * (df_model['post_type'] == 'figures')
    df_model['outside_link'] = 1 * (df_model['post_type'] == 'outside_link')

    #df_model[['figures', 'outside_link']] = pd.get_dummies(df_model['post_type'])[['figures', 'outside_link']]
    df_model['title_EQ_Norm'] = df_model['title_EQ']/df_model['title_length']
    after = dt.datetime(2021,1,1).timestamp()
    
    for row in range(df_model.shape[0]):
        df_model.loc[row, ['log_num', 'mean_upvotes']] = getAuthorFeatures(after, df_model.loc[row,'created'] - 1, df_model.loc[row,'subreddit'], df_model.loc[row,'author'])
    
    df_model = df_model.drop(columns = ['title','author','subreddit','ext_link','created','body','post_type','title_EQ','score'])

    return df_model

    

def get_reddit_info(url):
    Sub = reddit.submission(url = url)
    data={'score':[Sub.score],
              'body':[Sub.selftext],
              'created': [Sub.created_utc],
              'ext_link': [Sub.url],
              'title':[Sub.title],
              'subreddit':[Sub.subreddit.display_name],
              'author':[Sub.author.name]}
    return pd.DataFrame(data, index=None)

def process_data(input_url):
    df = get_reddit_info(input_url)
    df = featureProcessing(df)
    
    return df
    

    




    #df = prepare_score_label(df, ycol='score', threshold=1000)

def predict(X, mode):
    X = scaler.transform(X)
    
    if mode =='aggressive':
        threshold = 0.4
    else:
        threshold = 0.7
    


    return saved_model.predict_proba(X)[0,1] > threshold

def make_prediction(url, mode):
    X_input= process_data(url)
    pred = predict(X_input, mode)
    return pred

if __name__=="__main__":
    input_url = "https://www.reddit.com/r/postsreddit/comments/jjuci1/do_people_engage_more_when_you_post_an_earnest/"
    mode = 'aggressive'

    reddit = praw.Reddit(
        client_id="kxbUr-4PyE7DlQ",
        client_secret="Q5rIAPS9IHZ1QgOIkHNY09Y9VMxDsA",
        password="AACAXZDE",
        user_agent="testscript by u/kc_the_scraper",
        username="kc_the_scraper",
    )

    ## Load the model and the scaler
    with open("../03_predictive_models/saved_models/KC_0525_rf.sav", 'rb') as fmod:
        saved_model = pickle.load(fmod)
    with open("../03_predictive_models/saved_models/KC_0525_scaler.sav", 'rb') as fscal:
        scaler = pickle.load(fscal)    

    pred = make_prediction(input_url, mode)
    print (pred)


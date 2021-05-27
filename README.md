# Erdos Bootcamp 2021

## Team Members: 
- [Dyas Utomo](https://www.linkedin.com/in/dyasutomo/)
- [Ghanashyam Khanal](https://www.linkedin.com/in/ghanashyam-khanal/)
- [Kung-Ching Lin](https://www.linkedin.com/in/kung-ching-lin/)
- [Shahnawaz Khalid](https://www.linkedin.com/in/shahnawaz-khalid-252345116/)

## Introduction and Motivation

## Data gathering

### Reddit
- data for r/cryptocurrency can be read directly from (file size > 50MB) 
    `df_crypto = pd.read_csv('https://www.physics.rutgers.edu/~khanal/tmp/df_crypto.csv')`
- data for r/investing can be read from local file (small file size)
    `df_invest = pd.read_csv(ROOT_DIR+'01_data_gathering/df_investing.csv')`
- The complete database 'redditPosts.sqlite' (file size > 700MB) can be accessed via the following link https://drive.google.com/file/d/18QKkuO4c7gGXqYfq-Y2mZam_EUJyMFip/view?usp=sharing

### Twitter
- Data of all individual tweets with containing the phrases 'GameStop' and either $GME or #GME in the main body of the tweet from 12/25/2020 to 05/19/2021.
- TWEETS_individual contains each indiviual tweets along with its metrics: retweets, likes, replies and media.
- TWEETS_grouped contains twitter data grouped by each time period
- USERS contains meterics for each users profile and the metrics for the corresponding tweets in TWEETS_individual.


## Methodology

## Results

## Web Application

- Wrote a web application using streamlit and hosted on heroku on the `gristock.herokuapp.com`

## Future Work

# Erdos Bootcamp 2021

# Team Members: 
- [Dyas Utomo](https://www.linkedin.com/in/dyasutomo/)
- [Ghanashyam Khanal](https://www.linkedin.com/in/ghanashyam-khanal/)
- [Kung-Ching Lin](https://www.linkedin.com/in/kung-ching-lin/)
- [Shahnawaz Khalid](https://www.linkedin.com/in/shahnawaz-khalid-252345116/)

## Introduction and Motivation

# Data Gathering

Our dataset consists of all reddit posts from January 1, 2021 to mid May across several financial subreddits. Additionally, we have gathered tweets with certain keywords as well as the stock exchange data for the ticks of interest from the same period. In the following, we will describe the data by category.


## Reddit Posts (Main Contributor: Kung-Ching Lin)

There are two main APIs for reddit posts: PRAW and Pushshift. Although there are numerous features available, we chose to keep the following ones: subreddit, author, title, post body (texts in the posts if any), external links (links to figures, videos, or external websites), submission time, and score (total upvotes minus downvotes). The list of available features can be found here: [PRAW](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html), [Pushshift](https://github.com/pushshift/api).

### Trade-offs Between PRAW and Pushshift

The reason we use both APIs to obtain post information is because there are trade-offs between the two APIs. Pushshift is much quicker for data requests than PRAW but does not record real-time scores, as it maintains a copy of all reddit posts by updating continually. Thus, we needed to request information of all posts from Pushshift before retrieving the real-time score from PRAW by post ids. The corresponding file for data gathering can be found [here](https://github.com/kungchinglin/erdos_bootcamp_2021/blob/main/01_data_gathering/Data_gathering.ipynb).

### Dataset Description

We try to have a wide array of financial subreddits to see if there is any variance between them. The following table describes the number of posts we have for each subreddit. 

| Subreddit   | Number of Posts | Complete with Post Body?|
| ----------- | -----------     | ------------------- |
| r/wallstreetbets      | 954311           | No |
| r/dogecoin   | 576871        | No|
| r/CryptoCurrency   | 172461        | No|
| r/GME   | 152800        | Yes|
| r/amcstock   | 121480        | Yes|
| r/pennystocks   | 48514        | Yes|
| r/options   | 16589        | Yes|
| r/finance   | 2941        | Yes|
| r/Superstonks   | 146       | Yes|

Due to the low speed of PRAW, we were not able to complete gathering information for the top three subreddits. As such, we only worked on the subreddits with complete information.

## Twitter Data  (Main Contributor: Shahnawaz Khalid)

We used the new [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api) to obtain tweets from Dec 25th 2020 to May 20th 2021. We only focused on tweets that mentioned GameStop. To reduce the volume of 'spam' tweets or tweets with no information, we only searched for tweets that had the phrase "GameStop" and either the hashtag #GME or cashtag $GME mentioned in the text. We excluded tweets that were either retweets or replies and limited our search to tweets in english.

### Data Description

Each tweet comes with public metrics; likes, retweets and replies that we used as a basis for measuring popularity. The media attachment with the tweet, if any, was also saved and classified as either an image, video or animated gif. In addition we also pulled data for each user that tweeted that included, number of followers, number of tweets, number of users following and number of lists that the user was part of. These were later used as features for our models. The total number of tweets during this time period was 72823, comprising of 30496 uinque users. 

Finally, the reason GME has been so popular is because of its rapid increase in price. Therefore we extracted stock data consisting of open, close, high, low and volume from Yahoo Finance. However, because we are mainly interested in the changes in prices, we used daily returns, volatility (standard deviation of returns over 5 day window) and variation (square of the difference between log high and log low) as features for our models. 

# Exploratory Data Analysis

We have done some preliminary data analysis to explore our dataset. Though nothing too concrete can be derived, we have the following observations:

## Post Types
We split the reddit posts into three categories: posts with pictures/memes, posts with external links to either news or videos, and posts with only texts. Across different subreddits, we see a big difference:

![Meme ratio](./figures/meme_ratio.png)

We might be able to say that subreddits with a bunch of memes are less serious and may have a different criterion than the more serious ones for popularity.
    
In terms of upvotes, there are also differences across subreddits.

![Different Types](./figures/box_plots_different_types.png)

Even for meme-heavy subs, text-only posts still have a better potential of being highly upvoted, which is surprising.

## By Authors

We are also interested in whether authors should be included as one of the features in our data. It is expected that most posters have only ever submitted one post, while a small amount of them are more active. Examining the trends, we have the following figure:

![Author Contribution](./figures/author_contributions.png)

    
It can be seen that posters in GME and dogecoin have a much higher proportion of being highly active, with more than 5\% posters with more than 10 posts.

    
We also looked into other factors such as the time of the day and the text length. There are certain periods of times where the posts have a higher upvote ratio (upvotes/downvotes), so it indicates that including it as a feature may be sensible. For text lengths, it is harder to see a trend, though longer posts tend to be more upvoted for r/options.

## Time Dependency

![Upvotes vs Time](./figures/Popularity_vs_day_and_hour.png)

Here, we plot out the heatmap of popularity chances with respect to hour and day. It can be seen that there are apparent hot zones for post popularities. It suggests that the submission time does matter for prediction.

## Sensation Analysis

We can distinguish the types of posts by looking at some characteristics of the post: number of emojis used, number of uppercase letters, and the number of exclamation points/question marks. As they do contain information for predicting popularity, we end up including those.

![Number of Emoji Counts](./figures/Popularity_vs_emojis.png)

![Number of Uppercase Letters](./figures/Popularity_vs_uppercase.png)

![Number of Exclamation Points](./figures/Popularity_vs_exclamation.png)

It turns out that normalizing the number of exclamation points in the titles yields additional information.

![Normalized Number of Exclamation Points](./figures/normalized_title_EQ.png)

## Methodology

## Results

## Web Application

- Wrote a web application using streamlit and hosted on heroku on the `gristock.herokuapp.com`

## Future Work

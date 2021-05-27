I'm currently editing this. Let Dyas know if you want to make edit as well.

# Modeling

**Objective:** Our case is a binary classification: we predict popular posts, defined as the posts with top 5% percentile of scores.

**Features:** We include and combine the following features into TF-IDF:
1. Title of post
2. Body of post
3. Author's name
4. Subreddit forum
5. Sentiment analysis of the title
6. Posting time: day, date, and hour
7. Whether posts contain video/image or not?
8. The length of title text
9. The number of emoji in title and body
10. The number of exclamation and question marks in title and body
11. The number of upper and lower cases in title and body

**Data splitting:** We split the data (into training and test sets) by time. We use Jan-Mar posts as training set and April posts as test set.

We train and evaluate the data using the following models. When training, we modified the weight of the loss function by (100/x)-1, where x is the percentage of popular posts, to deal with imbalance date.

![picture](../figures/prec_rec_curve_summary_DU.png)

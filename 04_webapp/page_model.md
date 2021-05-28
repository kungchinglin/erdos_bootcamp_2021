# Modeling

**Objective:** Our case is a binary classification: we predict popular posts, defined as the posts with top 5% percentile of scores in each subreddit forum.

**Features:** We include the following features and combine them via TF-IDF and Word2Vec:
1. Title of post <br/>
2. Body of post <br/>
3. Author's name <br/>
4. Subreddit forum <br/>
5. Sentiment analysis of the title <br/>
6. Posting time: day, date, and hour <br/>
7. Whether that posts contain video/image or not? <br/>
8. The length of title text <br/>
9. The number of emoji in title and body <br/>
10. The number of exclamation and question marks in title and body <br/>
11. The number of upper and lower cases in title and body <br/>

**Data splitting:** We split the data (into training and test sets) by time. We use Jan-Mar posts as training set and April posts as test set.

**Training:** We train the following models: logistic regression, random forest classifier, XGBoost, and AdaBoost. To deal with imbalance data, we modified the weight of the loss function by (100/*x*)-1, where *x* is the percentage of popular posts.

**Model Performance:** We compare the models performace using the precision-recall curves.

![picture](../figures/prec_rec_curve_summary_DU.png)

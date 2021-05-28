# Modeling

## Objective
Our case is a binary classification: we predict popular posts, defined as the posts with top 5% percentile of scores in each subreddit forum.

## Data Splitting
Since there may be time dependency for what posts become popular in Reddit, we split the data (into training and test sets) by time. We use Jan-Mar posts as training set and April posts as test set. Among the training dataset, we tune the hyperparameters using 
```Python 
sklearn.model_selection.TimeSeriesSplit
``` 

## Features

From our exploratory data analysis, we considered the following features as our candidates for features.

1. Title of post <br/>
2. Body of post <br/>
3. Author's name <br/>
4. Subreddit forum <br/>
5. Sentiment analysis of the title <br/>
6. Posting time: day, date, and hour <br/>
7. Whether that posts contain video/image or not <br/>
8. The length of the title <br/>
9. The number of emoji counts in the title and the body <br/>
10. The number of exclamation points and question marks in the title and the body <br/>
11. The number of upper and lower cases in the title and the body <br/>
12. The number of tweets, likes, and retweets with specific keywords three days preceding the post submission

## Evaluation Metrics

The stakeholders of this project are the traders of the firm, and we believe they will be interested in seeing high precision and/or high recall rate depending on their purposes. If a significant amount of money is involved based on the prediction outcome, then increasing the precision will be paramount. On the other hand, if only an exploration of what are potentially popular is needed, then having high recall will be more appropriate.

With that in mind, we evaluate our models based on precision-recall curves, with an emphasis for high precision. In our deployed model, the user can freely choose whether they want to be aggressive (high recall) or conservative (high precision).

## Model Selection

We have proposed several versions of modeling approaches, each of which yielding similar performance and has room for improvement. It suggests that the features we select may be insufficient for predicting the popularity (high bias).



**Features:** We include the following features and combine them via TF-IDF and Word2Vec:

**Training:** We train the following models: logistic regression, random forest classifier, XGBoost, and AdaBoost. To deal with imbalance data, we modified the weight of the loss function by (100/*x*)-1, where *x* is the percentage of popular posts.

**Model Performance:** We compare the models performace using the precision-recall curves. As shown below, model perfomances are more or less similar, but XGBoost gives the best performance.

![picture](../figures/prec_rec_curve_summary_DU.png)

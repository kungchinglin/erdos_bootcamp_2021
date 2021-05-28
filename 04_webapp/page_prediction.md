# Manual

This web app is for predicting whether a reddit post will go viral. To use it, please input the url to the reddit post you want to predict. As of now, we have only tested on posts in selected financial subreddits, though you are welcome to try out other subreddits.

## Strategies

You can also determine your strategy in predicting post popularity. If you don't want to miss out on potentially popular posts, you may choose the strategy to be "Aggressive", which means more posts will be flagged as popular, at the expense of lower precision (More posts misclassified as popular). On the other hand, if you don't want to sift through a lot of unpopular posts, you may choose to be "Defensive". It makes sure that the precision is high, but you may miss out on other popular posts (low recall).

## Outcomes

The outcome is either "Viral" or "Non-viral". We defined viral posts as ones in the top 5 percentile of that subreddit in terms of upvotes.

## Implementation Detail

To see how the model is built, please explore the side bar on the left for more information. To see details of the implementation, please refer to our [Github](https://github.com/kungchinglin/erdos_bootcamp_2021) page.

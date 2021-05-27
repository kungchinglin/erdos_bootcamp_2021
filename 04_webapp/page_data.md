# Data Gathering

Our dataset consists of all reddit posts from January 1, 2021 to mid May across several financial subreddits. Additionally, we have gathered tweets with certain keywords as well as the stock exchange data for the ticks of interest from the same period. In the following, we will describe the data by category.


## Reddit Posts

There are two main APIs for reddit posts: PRAW and Pushshift. Although there are numerous features available, we chose to keep the following ones: subreddit, author, title, post body (texts in the posts if any), external links (links to figures, videos, or external websites), submission time, and score (total upvotes minus downvotes). The list of available features can be found here: [PRAW](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html), [Pushshift](https://github.com/pushshift/api).

### Trade-offs Between PRAW and Pushshift

The reason we use both APIs to obtain post information is because there are trade-offs between the two APIs. Pushshift is much quicker for data requests than PRAW but does not record real-time scores, as it maintains a copy of all reddit posts by updating continually. Thus, we needed to request information of all posts from Pushshift before retrieving the real-time score from PRAW by post ids.

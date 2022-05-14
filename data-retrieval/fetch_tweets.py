from datetime import datetime, timedelta
import re
import snscrape.modules.twitter as sntwitter


def fetch_tweets_by_search_term(search_term):
    tweets_list1 = []
    now = datetime.now()
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'%24{search_term}').get_items()):
        if now - timedelta(hours=1) > tweet.date or i >= 100:
            break
        tweets_list1.append(clean_tweet(tweet.content))

    return tweets_list1


def clean_tweet(tweet):
    # Remove all @'s
    clean_tweet = re.sub("@[A-Za-z0-9_]+", "", tweet)
    # Remove all links
    clean_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', clean_tweet)
    # Remove all hashtags
    # clean_tweet = re.sub("#[A-Za-z0-9_]+","", clean_tweet)
    return clean_tweet

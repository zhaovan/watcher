import credentials
import tweepy
import csv
import json


def fetch_tweets():
    auth = tweepy.OAuthHandler(credentials.api_key, credentials.api_key_secret)
    auth.set_access_token(credentials.access_token,
                          credentials.access_token_secret)

    api = tweepy.API(auth)

    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(count=200)

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(count=200, max_id=oldest)

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print(f"...{len(all_tweets)} tweets downloaded so far")

    # transform the tweepy tweets into a 2D array that will populate the csv

    # https://twitter.com/zhaovan8/status/1458182530226610185

    outtweets = [{"id": tweet.id_str, "text": tweet.text}
                 for tweet in all_tweets]

    # write the csv
    with open(f'new_zhaovan8_tweets.json', 'w') as f:
        json.dump(outtweets, f)

    pass


fetch_tweets()

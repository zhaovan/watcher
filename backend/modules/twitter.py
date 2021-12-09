

import nltk
from nltk.tokenize import word_tokenize, regexp_tokenize
import json
nltk.download('punkt')


def read_tweets(file_path):
    with open(file_path) as f:
        tweetsJSON = json.load(f)
    tweet_map = []
    for i in range(len(tweetsJSON)):
        curr_tweet = tweetsJSON[i]
        print(curr_tweet)
        if (i % 100 == 0):
            print(str(i) + " number of tweets have been read so far")

        tweet_map.append({
            "id": "tw" + str(i),
            "tokens": word_tokenize(curr_tweet["text"]),
            # "tokens": regexp_tokenize(curr_tweet["text"], pattern=r"\s|[\.,;']", gaps=True),
            "content": curr_tweet["text"],
            "href": "https://twitter.com/zhaovan8/status/" + curr_tweet["id"]})

    print(tweet_map)


read_tweets("tweets.json")

import json
import sys
sys.path.append("/Users/ivanzhao/Documents/GitHub/watcher")
from lib.tokenizer import Tokenizer

def read_tweets(file_path):
    with open(file_path) as f:
        tweetsJSON = json.load(f)
    tweet_list = []
    for i in range(len(tweetsJSON)):
        curr_tweet = tweetsJSON[i]
        
        if (i % 100 == 0):
            print(str(i) + " number of tweets have been read so far")

        tokenizer = Tokenizer()
        token_map = tokenizer.tokenize_words(curr_tweet["text"], False)

        # add the token to docs
        tweet_list.append({
            "id": "tw" + str(i),
            "tokens": token_map,
            
            "content": curr_tweet["text"],
            "href": "https://twitter.com/zhaovan8/status/" + curr_tweet["id"]})

    return tweet_list


curr_twitter_map = read_tweets("tweets.json")

with open("tweet_doc.json", "w") as f:
    json.dump(curr_twitter_map, f)

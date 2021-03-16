import tweepy as tweepy
import webbrowser as webbrowser

import time

consumer_key = "wKjvYJ6LocuUd9qxmK4W5PxAt"
consumer_secret = "rGwNVozddHRcZnFVwvf5e8gi1kAaDgj2YWtAojBG5rFPKU8WSu"

callback_uri = 'oob'  # url

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
redirect_url = auth.get_authorization_url()
print(redirect_url)

webbrowser.open(redirect_url)
user_pint_input = input("What's the pin value")
auth.get_access_token(user_pint_input)

api = tweepy.API(auth)

me = api.me()


def work(searchterm):
    maxTweets = 50
    tweetsdata = tweepy.Cursor(api.search, q=searchterm).items(maxTweets)

    return tweetsdata


def workSentiment(searchterms):
    mean = 0
    n = 0
    # total = 0
    for tweets in searchterms:
        # total = sentiment(tweets)
        n = n + 1
        # mean = ((mean * n-1) + total)/n

    return mean

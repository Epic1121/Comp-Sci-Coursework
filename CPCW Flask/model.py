import tweepy as tweepy
import webbrowser as webbrowser
import os
import argparse
from google.cloud import language_v1
from google.cloud.language_v1.types import language_service



# Twitter setup

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

# Cloud sentiment setup

credentials_path = r'C:\Users\joshg\Programming\CPCW Flask\CloudPrivateKeyJSON\Computing Coursework-58c6f75f68aa.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

client = language_v1.LanguageServiceClient()
type_ = language_v1.Document.Type.PLAIN_TEXT
language = "en"


def work(searchterm):
    maxTweets = 50
    tweetsdata = tweepy.Cursor(api.search, q=searchterm).items(maxTweets)
    sentiment = workSentiment(tweetsdata)
    return sentiment


def workSentiment(searchterms):
    mean = 0
    n = 0
    total = 0
    for tweets in searchterms:
        document = {"content": tweets.text, "type": type_, "language": language}

        encoding_type = language_v1.EncodingType.UTF8

        # sentiment = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
        # print(u"Document sentiment score: {}".format(sentiment.document_sentiment.score))

        document = language_v1.Document(content=tweets.text)

        sentiment = client.analyze_sentiment(document=document).document_sentiment

        n = n + 1
        mean = ((mean * n-1) + sentiment.document_sentiment.score)/n

    return mean

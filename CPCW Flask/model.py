import tweepy
import webbrowser
import os
from google.cloud import language_v1


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


def work(search_term):
    """
    This Function searches twitter for tweets
    :param search_term: The search term passed in to search
    :return: the average sentiment
    """

    i = 0
    max_Tweets = int(10)
    tweets_data = tweepy.Cursor(api.search, q=search_term).items(max_Tweets)
    for tweet in tweets_data:
        i = i + 1

    if i != 0:
        sentiment = workSentiment(tweets_data, i)
    else:
        sentiment = float(0)

    return sentiment


def workSentiment(data, totalint):
    """
    This function divides the tweets into individual strings, which then are calculated the sentiment of

    :param data: the tweets data gathered
    :param totalint: the total number of tweets
    :return: the mean sentiment
    """
    total = 0
    for tweets in data:

        sentiment = sample_analyze_sentiment(tweets.text)
        total = total + sentiment

    mean = total/totalint

    return mean


def sample_analyze_sentiment(text_content):
    """
    This function Analyzes Sentiment in a String

    :param text_content: The string text content to analyze
    :return: sentiment gathered from the string passed in
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )

    return response.document_sentiment.score

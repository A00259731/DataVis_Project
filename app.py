from flask import Flask, render_template, request

import tweepy as tp
import os
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

from twitter_auth import *

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tp.API(auth)

app = Flask(__name__)

def percentage(part, whole):
    return 100 * float(part)/float(whole)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def aboutpage():
    return render_template('about.html')

@app.route('/part1', methods=['POST'])
def part1():
    query = 'Budget2022'
    tweets = tp.Cursor(api.search, q=query).items(50)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []

    for tweet in tweets:
        #print(tweet.text)
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        sentiment = TextBlob(tweet.text).sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
            sentiment = "neu"

        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
            sentiment = "neg"

        elif (analysis.sentiment.polarity > 0.00):
            positive += 1
            sentiment = "pos"

        tweet_list.append((tweet.text, sentiment))

    df = pd.DataFrame(tweet_list)

    positive = str(percentage(positive, 10))
    #print(positive)
    negative = str(percentage(negative, 10))
    #print(negative)
    neutral = str(percentage(neutral, 10))
    #print(neutral)

    if os.path.exists("/part1textblob.csv"):
        os.remove("part1textblob.csv")
        df.to_csv("part1textblob.csv", sep=",")
    else:
        df.to_csv("part1textblob.csv", sep=",")


    return render_template('part1.html', pos_result = positive, neg_result = negative, neu_result = neutral, query = tweets, tlist= tweet_list)

    return render_template('404.html')

@app.route('/part2', methods=['POST'])
def part2():
    query="Budget2022"

    tweets = tp.Cursor(api.search, q=query).items(50)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neu_list = []
    pos_list = []
    neg_list = []
    neg_loc_ire = 0
    neg_loc_eng = 0
    neg_loc_oth = 0
    neu_loc_ire = 0
    neu_loc_eng = 0
    neu_loc_oth = 0
    pos_loc_ire = 0
    pos_loc_eng = 0
    pos_loc_oth = 0
    sentiment = ""

    for tweet in tweets:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        location = str(tweet.user.location)

        if "Ireland" in location:
            location = "Ireland"
        elif "England" in location:
            location = "England"
        else:
            location = "Not given"

        if neg > pos:
            negative += 1
            neu_list.append(location)
            sentiment = "neg"
        elif pos > neg:
            positive += 1
            sentiment = "pos"
            neg_list.append(location)
        elif pos == neg:
            neutral += 1
            sentiment = "neu"
            pos_list.append(location)

        tweet_list.append((tweet.text,sentiment,location))

    df = pd.DataFrame(tweet_list)

    if os.path.exists("/part2vader.csv"):
        os.remove("part2vader.csv")
        df.to_csv("part2vader.csv", sep=",")
    else:
        df.to_csv("part2vader.csv", sep=",")

    positive = str(percentage(positive, 10))
    #print(positive)
    negative = str(percentage(negative, 10))
    #print(negative)
    neutral = str(percentage(neutral, 10))
    #print(neutral)

    print(polarity)
    return render_template('part2.html', pos_result = positive, neg_result = negative, neu_result = neutral, query = tweets)


@app.route('/tweets', methods=['POST'])
def tweetspage():

    if request.method == 'POST':
        query = request.form['tweet']
        tweets = tp.Cursor(api.search, q=query).items(10)

        return render_template('results.html', query = tweets)

    return render_template('404.html')




if __name__ == '__main__':
    app.run()

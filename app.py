from flask import Flask, render_template, request

import tweepy as tp
import os
import json
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
    tweets = tp.Cursor(api.search, q=query).items(100)

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
    negative = str(percentage(negative, 100))
    #print(negative)
    neutral = str(percentage(neutral, 100))
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

    tweets = tp.Cursor(api.search, q=query).items(100)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    sentiment = ""

    for tweet in tweets:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']

        if neg > pos:
            negative += 1
            sentiment = "neg"
        elif pos > neg:
            positive += 1
            sentiment = "pos"
        elif pos == neg:
            neutral += 1
            sentiment = "neu"

        tweet_list.append((tweet.text,sentiment))

    df = pd.DataFrame(tweet_list)

    if os.path.exists("/part2vader.csv"):
        os.remove("part2vader.csv")
        df.to_csv("part2vader.csv", sep=",")
    else:
        df.to_csv("part2vader.csv", sep=",")

    positive = str(percentage(positive, 100))
    #print(positive)
    negative = str(percentage(negative, 100))
    #print(negative)
    neutral = str(percentage(neutral, 100))
    #print(neutral)

    print(polarity)
    return render_template('part2.html', pos_result = positive, neg_result = negative, neu_result = neutral, query = tweets)

@app.route('/part3', methods=['POST'])
def part3():
    query = "Budget2022"

    tweets = tp.Cursor(api.search, q=query).items(100)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    sentiment = ""
    client = ""
    pos_client_android = 0
    pos_client_iphone = 0
    pos_client_web = 0
    pos_client_other = 0
    neu_client_android = 0
    neu_client_iphone = 0
    neu_client_web = 0
    neu_client_other = 0
    neg_client_android = 0
    neg_client_iphone = 0
    neg_client_web = 0
    neg_client_other = 0

    for tweet in tweets:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        source = tweet.source;

        if neg > pos:
            negative += 1
            sentiment = "neg"
            if "android" in source.lower():
                client = "Android"
                neg_client_android += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neg_client_iphone += 1
            elif "web" in source.lower():
                client = "Browser"
                neg_client_web += 1
            else:
                client = "Other"
                neg_client_other += 1
        elif pos > neg:
            positive += 1
            sentiment = "pos"
            if "android" in source.lower():
                client = "Android"
                pos_client_android += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                pos_client_iphone += 1
            elif "web" in source.lower():
                client = "Browser"
                pos_client_web += 1
            else:
                client = "Other"
                pos_client_other += 1
        elif pos == neg:
            neutral += 1
            sentiment = "neu"
            if "android" in source.lower():
                client = "Android"
                neu_client_android += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neu_client_iphone += 1
            elif "web" in source.lower():
                client = "Browser"
                neu_client_web += 1
            else:
                client = "Other"
                neu_client_other += 1

        tweet_list.append((tweet.text, sentiment, client))

    df = pd.DataFrame(tweet_list)

    if os.path.exists("/part3drilldown.csv"):
        os.remove("part3drilldown.csv")
        df.to_csv("part3drilldown.csv", sep=",")
    else:
        df.to_csv("part3drilldown.csv", sep=",")

    positive = str(percentage(positive, 100))

    negative = str(percentage(negative, 100))

    neutral = str(percentage(neutral, 100))

    pos_client_android = str(percentage(pos_client_android, 100))
    pos_client_iphone = str(percentage(pos_client_iphone, 100))
    pos_client_web = str(percentage(pos_client_web, 100))
    pos_client_other = str(percentage(pos_client_other, 100))
    neu_client_android = str(percentage(neu_client_android, 100))
    neu_client_iphone = str(percentage(neu_client_iphone, 100))
    neu_client_web = str(percentage(neu_client_web, 100))
    neu_client_other = str(percentage(neu_client_other, 100))
    neg_client_android = str(percentage(neg_client_android, 100))
    neg_client_iphone = str(percentage(neg_client_iphone, 100))
    neg_client_web = str(percentage(neg_client_web, 100))
    neg_client_other = str(percentage(neg_client_other, 100))
    return render_template('part3.html', pos_result = positive, neg_result = negative,
                           neu_result = neutral, query = tweets, neu_c_a = neu_client_android,
                           neu_c_ip = neu_client_iphone, neu_c_w= neu_client_web, neu_c_o = neu_client_other,
                           neg_c_a=neg_client_android, neg_c_ip=neg_client_iphone, neg_c_w=neg_client_web,
                           neg_c_o=neg_client_other,  pos_c_a = pos_client_android, pos_c_ip = pos_client_iphone,
                           pos_c_w= pos_client_web, pos_c_o = pos_client_other,)


@app.route('/part4', methods=['POST'])
def part4():
    query1 = "Final Fantasy XIV"

    tweets1 = tp.Cursor(api.search, q=query1).items(100)

    positive1 = 0
    negative1 = 0
    neutral1 = 0
    polarity = 0
    tweet_list1 = []
    sentiment = ""
    client = ""
    pos_client_android1 = 0
    pos_client_iphone1 = 0
    pos_client_web1 = 0
    pos_client_other1 = 0
    neu_client_android1 = 0
    neu_client_iphone1 = 0
    neu_client_web1 = 0
    neu_client_other1 = 0
    neg_client_android1 = 0
    neg_client_iphone1 = 0
    neg_client_web1 = 0
    neg_client_other1 = 0

    for tweet in tweets1:
        score1 = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score1['neg']
        neu = score1['neu']
        pos = score1['pos']
        comp = score1['compound']
        source = tweet.source;

        if neg > pos:
            negative1 += 1
            sentiment = "neg"
            if "android" in source.lower():
                client = "Android"
                neg_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neg_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                neg_client_web1 += 1
            else:
                client = "Other"
                neg_client_other1 += 1
        elif pos > neg:
            positive1 += 1
            sentiment = "pos"
            if "android" in source.lower():
                client = "Android"
                pos_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                pos_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                pos_client_web1 += 1
            else:
                client = "Other"
                pos_client_other1 += 1
        elif pos == neg:
            neutral1 += 1
            sentiment = "neu"
            if "android" in source.lower():
                client = "Android"
                neu_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neu_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                neu_client_web1 += 1
            else:
                client = "Other"
                neu_client_other1 += 1

        tweet_list1.append((tweet.text, sentiment, client))

    df = pd.DataFrame(tweet_list1)

    positive1 = str(percentage(positive1, 100))

    negative1 = str(percentage(negative1, 100))

    neutral1 = str(percentage(neutral1, 100))

    pos_client_android1 = str(percentage(pos_client_android1, 100))
    pos_client_iphone1 = str(percentage(pos_client_iphone1, 100))
    pos_client_web1 = str(percentage(pos_client_web1, 100))
    pos_client_other1 = str(percentage(pos_client_other1, 100))
    neu_client_android1 = str(percentage(neu_client_android1, 100))
    neu_client_iphone1 = str(percentage(neu_client_iphone1, 100))
    neu_client_web1 = str(percentage(neu_client_web1, 100))
    neu_client_other1 = str(percentage(neu_client_other1, 100))
    neg_client_android1 = str(percentage(neg_client_android1, 100))
    neg_client_iphone1 = str(percentage(neg_client_iphone1, 100))
    neg_client_web1 = str(percentage(neg_client_web1, 100))
    neg_client_other1 = str(percentage(neg_client_other1, 100))

    query2 = "World of Warcraft"

    tweets2 = tp.Cursor(api.search, q=query2).items(100)

    positive2 = 0
    negative2 = 0
    neutral2 = 0
    polarity = 0
    tweet_list2 = []
    sentiment = ""
    client = ""
    pos_client_android2 = 0
    pos_client_iphone2 = 0
    pos_client_web2 = 0
    pos_client_other2 = 0
    neu_client_android2 = 0
    neu_client_iphone2 = 0
    neu_client_web2 = 0
    neu_client_other2 = 0
    neg_client_android2 = 0
    neg_client_iphone2 = 0
    neg_client_web2 = 0
    neg_client_other2 = 0

    for tweet in tweets2:
        score2 = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score2['neg']
        neu = score2['neu']
        pos = score2['pos']
        comp = score2['compound']
        source = tweet.source;

        if neg > pos:
            negative2 += 1
            sentiment = "neg"
            if "android" in source.lower():
                client = "Android"
                neg_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neg_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                neg_client_web2 += 1
            else:
                client = "Other"
                neg_client_other2 += 1
        elif pos > neg:
            positive2 += 1
            sentiment = "pos"
            if "android" in source.lower():
                client = "Android"
                pos_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                pos_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                pos_client_web2 += 1
            else:
                client = "Other"
                pos_client_other2 += 1
        elif pos == neg:
            neutral2 += 1
            sentiment = "neu"
            if "android" in source.lower():
                client = "Android"
                neu_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neu_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                neu_client_web2 += 1
            else:
                client = "Other"
                neu_client_other2 += 1

        tweet_list2.append((tweet.text, sentiment, client))

    df = pd.DataFrame(tweet_list2)

    positive2 = str(percentage(positive2, 100))

    negative2 = str(percentage(negative2, 100))

    neutral2 = str(percentage(neutral2, 100))

    pos_client_android2 = str(percentage(pos_client_android2, 100))
    pos_client_iphone2 = str(percentage(pos_client_iphone2, 100))
    pos_client_web2 = str(percentage(pos_client_web2, 100))
    pos_client_other2 = str(percentage(pos_client_other2, 100))
    neu_client_android2 = str(percentage(neu_client_android2, 100))
    neu_client_iphone2 = str(percentage(neu_client_iphone2, 100))
    neu_client_web2 = str(percentage(neu_client_web2, 100))
    neu_client_other2 = str(percentage(neu_client_other2, 100))
    neg_client_android2 = str(percentage(neg_client_android2, 100))
    neg_client_iphone2 = str(percentage(neg_client_iphone2, 100))
    neg_client_web2 = str(percentage(neg_client_web2, 100))
    neg_client_other2 = str(percentage(neg_client_other2, 100))

    return render_template('part4.html', topic1= query1, pos_result1 = positive1, neg_result1 = negative1,
                           neu_result1 = neutral1, query1 = tweets1, neu_c_a1 = neu_client_android1,
                           neu_c_ip1 = neu_client_iphone1, neu_c_w1= neu_client_web1, neu_c_o1 = neu_client_other1,
                           neg_c_a1=neg_client_android1, neg_c_ip1=neg_client_iphone1, neg_c_w1=neg_client_web1,
                           neg_c_o1=neg_client_other1,  pos_c_a1 = pos_client_android1, pos_c_ip1 = pos_client_iphone1,
                           pos_c_w1= pos_client_web1, pos_c_o1 = pos_client_other1, topic2= query2, pos_result2 = positive2, neg_result2 = negative2,
                           neu_result2 = neutral2, query2 = tweets2, neu_c_a2 = neu_client_android2,
                           neu_c_ip2 = neu_client_iphone2, neu_c_w2= neu_client_web2, neu_c_o2 = neu_client_other2,
                           neg_c_a2=neg_client_android2, neg_c_ip2=neg_client_iphone2, neg_c_w2=neg_client_web2,
                           neg_c_o2=neg_client_other2,  pos_c_a2 = pos_client_android2, pos_c_ip2 = pos_client_iphone2,
                           pos_c_w2= pos_client_web2, pos_c_o2 = pos_client_other2,)

@app.route('/part4.', methods=['POST'])
def chosentopics():


    if request.method == 'POST':
        global query1
        query1 = request.form['topic1']

    if request.method == 'POST':
        global query2
        query2 = request.form['topic2']


    tweets1 = tp.Cursor(api.search, q=query1).items(100)

    positive1 = 0
    negative1 = 0
    neutral1 = 0
    polarity = 0
    tweet_list1 = []
    sentiment = ""
    client = ""
    pos_client_android1 = 0
    pos_client_iphone1 = 0
    pos_client_web1 = 0
    pos_client_other1 = 0
    neu_client_android1 = 0
    neu_client_iphone1 = 0
    neu_client_web1 = 0
    neu_client_other1 = 0
    neg_client_android1 = 0
    neg_client_iphone1 = 0
    neg_client_web1 = 0
    neg_client_other1 = 0

    for tweet in tweets1:
        score1 = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score1['neg']
        neu = score1['neu']
        pos = score1['pos']
        comp = score1['compound']
        source = tweet.source;

        if neg > pos:
            negative1 += 1
            sentiment = "neg"
            if "android" in source.lower():
                client = "Android"
                neg_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neg_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                neg_client_web1 += 1
            else:
                client = "Other"
                neg_client_other1 += 1
        elif pos > neg:
            positive1 += 1
            sentiment = "pos"
            if "android" in source.lower():
                client = "Android"
                pos_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                pos_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                pos_client_web1 += 1
            else:
                client = "Other"
                pos_client_other1 += 1
        elif pos == neg:
            neutral1 += 1
            sentiment = "neu"
            if "android" in source.lower():
                client = "Android"
                neu_client_android1 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neu_client_iphone1 += 1
            elif "web" in source.lower():
                client = "Browser"
                neu_client_web1 += 1
            else:
                client = "Other"
                neu_client_other1 += 1

        tweet_list1.append((tweet.text, sentiment, client))

    df = pd.DataFrame(tweet_list1)

    positive1 = str(percentage(positive1, 100))

    negative1 = str(percentage(negative1, 100))

    neutral1 = str(percentage(neutral1, 100))

    pos_client_android1 = str(percentage(pos_client_android1, 100))
    pos_client_iphone1 = str(percentage(pos_client_iphone1, 100))
    pos_client_web1 = str(percentage(pos_client_web1, 100))
    pos_client_other1 = str(percentage(pos_client_other1, 100))
    neu_client_android1 = str(percentage(neu_client_android1, 100))
    neu_client_iphone1 = str(percentage(neu_client_iphone1, 100))
    neu_client_web1 = str(percentage(neu_client_web1, 100))
    neu_client_other1 = str(percentage(neu_client_other1, 100))
    neg_client_android1 = str(percentage(neg_client_android1, 100))
    neg_client_iphone1 = str(percentage(neg_client_iphone1, 100))
    neg_client_web1 = str(percentage(neg_client_web1, 100))
    neg_client_other1 = str(percentage(neg_client_other1, 100))

    tweets2 = tp.Cursor(api.search, q=query2).items(100)

    positive2 = 0
    negative2 = 0
    neutral2 = 0
    polarity = 0
    tweet_list2 = []
    sentiment = ""
    client = ""
    pos_client_android2 = 0
    pos_client_iphone2 = 0
    pos_client_web2 = 0
    pos_client_other2 = 0
    neu_client_android2 = 0
    neu_client_iphone2 = 0
    neu_client_web2 = 0
    neu_client_other2 = 0
    neg_client_android2 = 0
    neg_client_iphone2 = 0
    neg_client_web2 = 0
    neg_client_other2 = 0

    for tweet in tweets2:
        score2 = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        neg = score2['neg']
        neu = score2['neu']
        pos = score2['pos']
        comp = score2['compound']
        source = tweet.source;

        if neg > pos:
            negative2 += 1
            sentiment = "neg"
            if "android" in source.lower():
                client = "Android"
                neg_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neg_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                neg_client_web2 += 1
            else:
                client = "Other"
                neg_client_other2 += 1
        elif pos > neg:
            positive2 += 1
            sentiment = "pos"
            if "android" in source.lower():
                client = "Android"
                pos_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                pos_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                pos_client_web2 += 1
            else:
                client = "Other"
                pos_client_other2 += 1
        elif pos == neg:
            neutral2 += 1
            sentiment = "neu"
            if "android" in source.lower():
                client = "Android"
                neu_client_android2 += 1
            elif "iphone" in source.lower():
                client = "iPhone"
                neu_client_iphone2 += 1
            elif "web" in source.lower():
                client = "Browser"
                neu_client_web2 += 1
            else:
                client = "Other"
                neu_client_other2 += 1

        tweet_list2.append((tweet.text, sentiment, client))

    df = pd.DataFrame(tweet_list2)

    positive2 = str(percentage(positive2, 100))

    negative2 = str(percentage(negative2, 100))

    neutral2 = str(percentage(neutral2, 100))

    pos_client_android2 = str(percentage(pos_client_android2, 100))
    pos_client_iphone2 = str(percentage(pos_client_iphone2, 100))
    pos_client_web2 = str(percentage(pos_client_web2, 100))
    pos_client_other2 = str(percentage(pos_client_other2, 100))
    neu_client_android2 = str(percentage(neu_client_android2, 100))
    neu_client_iphone2 = str(percentage(neu_client_iphone2, 100))
    neu_client_web2 = str(percentage(neu_client_web2, 100))
    neu_client_other2 = str(percentage(neu_client_other2, 100))
    neg_client_android2 = str(percentage(neg_client_android2, 100))
    neg_client_iphone2 = str(percentage(neg_client_iphone2, 100))
    neg_client_web2 = str(percentage(neg_client_web2, 100))
    neg_client_other2 = str(percentage(neg_client_other2, 100))

    return render_template('part4.html', topic1=query1, pos_result1=positive1, neg_result1=negative1,
                           neu_result1=neutral1, query1=tweets1, neu_c_a1=neu_client_android1,
                           neu_c_ip1=neu_client_iphone1, neu_c_w1=neu_client_web1, neu_c_o1=neu_client_other1,
                           neg_c_a1=neg_client_android1, neg_c_ip1=neg_client_iphone1, neg_c_w1=neg_client_web1,
                           neg_c_o1=neg_client_other1, pos_c_a1=pos_client_android1, pos_c_ip1=pos_client_iphone1,
                           pos_c_w1=pos_client_web1, pos_c_o1=pos_client_other1, topic2=query2, pos_result2=positive2,
                           neg_result2=negative2,
                           neu_result2=neutral2, query2=tweets2, neu_c_a2=neu_client_android2,
                           neu_c_ip2=neu_client_iphone2, neu_c_w2=neu_client_web2, neu_c_o2=neu_client_other2,
                           neg_c_a2=neg_client_android2, neg_c_ip2=neg_client_iphone2, neg_c_w2=neg_client_web2,
                           neg_c_o2=neg_client_other2, pos_c_a2=pos_client_android2, pos_c_ip2=pos_client_iphone2,
                           pos_c_w2=pos_client_web2, pos_c_o2=pos_client_other2, )


    return render_template('part4.html')


    return render_template('404.html')

@app.route('/tweets', methods=['POST'])
def tweetspage():

    if request.method == 'POST':
        query = request.form['tweet']
        tweets = tp.Cursor(api.search, q=query).items(10)

        return render_template('results.html', query = tweets)

    return render_template('404.html')

if __name__ == '__main__':
    app.run()

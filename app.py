from flask import Flask, render_template, request

import tweepy as tp
from textblob import TextBlob
import vader as vr;

from twitter_auth import *

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tp.API(auth)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def aboutpage():
    return render_template('about.html')

@app.route('/part1', methods=['POST'])
def part1():
    query = 'trump'
    tweets = tp.Cursor(api.search, q=query).items(10)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    for tweet in tweets:
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
        elif (analysis.sentiment.polarity > 0.00):
            positive += 1

    positive = str(percentage(positive, 10))
    print(positive)
    negative = str(percentage(positive, 10))
    print(negative)
    neutral = str(percentage(positive, 10))
    print(neutral)

    return render_template('part1.html', pos_result = positive, neg_result = negative, neu_result = neutral, query = tweets)

    return render_template('404.html')

@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['tweet']
        tweets = tp.Cursor(api.search, q=query).items(10)

        return render_template('results.html', query = tweets)

    return render_template('404.html')




if __name__ == '__main__':
    app.run()

def percentage(part, whole):
    return 100 * float(part)/float(whole)

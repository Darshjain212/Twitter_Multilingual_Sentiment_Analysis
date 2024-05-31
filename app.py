import re 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer
import re 
import pandas as pd
from flask import Flask, render_template , redirect, url_for, request
import pandas as pd
import scaping
import numpy as np

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()

def clean_tweet( tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment(tweet): 

    sentiment_scores = analyzer.polarity_scores(tweet)

    if sentiment_scores['compound'] >= 0.05:
        return 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def get_tweets(query, count): 
        
        count = int(count)
        tweets = []
        fetched_tweets,untranslateed = scaping.get_tweets(query,count)
        count_P=0
        count_N=0    
        for tweet in fetched_tweets:     
            parsed_tweet = {} 
            parsed_tweet['text']=clean_tweet(tweet)
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet) 
            if(parsed_tweet['sentiment']=="positive"):
                count_P+=1
            elif(parsed_tweet['sentiment']=="negative"):
                count_N+=1
            tweets.append(parsed_tweet) 
        overall="Positive" if count_P>count_N else "Negative"
        return tweets,untranslateed,overall


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            fetched_tweets,tweets,overall = get_tweets(query, count) 
            return render_template('result.html', result=zip(fetched_tweets,tweets) , overall_r=overall)


@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            sentiment_scores = analyzer.polarity_scores(text)
            if sentiment_scores['compound'] >= 0.05:
                text_sentiment =  'positive'
            elif sentiment_scores['compound'] <= -0.05:
                text_sentiment  = 'negative'
            else:
                text_sentiment = 'neutral'
            return render_template('result1.html',msg=text, result=text_sentiment)
        
      



if __name__ == '__main__':
    app.debug=True
    app.run(host='localhost', port=5000)
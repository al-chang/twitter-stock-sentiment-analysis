from datetime import datetime
import sched
import time
import pickle
import os
import firebase_admin
import threading
import logging
from dotenv import load_dotenv
from firebase_admin import db
from fetch_tweets import fetch_tweets_by_search_term

load_dotenv()

STOCKS = ["MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DOW", "GS", "HD", "HON",
          "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT"]

# Set up firebase connection
databaseURL = os.environ.get("DATABASE_URL")
cred_obj = firebase_admin.credentials.Certificate('firebase-key.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})


def add_stock_sentiment_entry(stock_ticker, num_pos, total):
    ref = db.reference(f"/Stock/{stock_ticker}")
    ref.push().set({
        "time": datetime.now().isoformat(),
        "num_pos": num_pos,
        "total": total
    })


# Set up ML model
with open("finalized_model.sav", "rb") as f:
    model = pickle.load(f)
print("Model loaded")

with open("vectorizer.sav", "rb") as f:
    vect = pickle.load(f)
print('Vectorizer loaded')


def process_tweets(tweets):
    num_pos = 0
    for tweet in tweets:
        comment_features = vect.transform([tweet])
        sentiment = model.predict(comment_features)
        if sentiment == 1:
            num_pos += 1

    return num_pos, len(tweets)


# Run scheduler
s = sched.scheduler(time.time, time.sleep)


def update_stock_data(stock_ticker):
    tweets = fetch_tweets_by_search_term(stock_ticker)
    num_pos, total = process_tweets(tweets)
    add_stock_sentiment_entry(stock_ticker, num_pos, total)


def perform_tweet_analysis(sc: sched.scheduler):
    for stock_ticker in STOCKS:
        update_stock_data(stock_ticker)

    sc.enter(time_to_seconds(hours=6), 1, perform_tweet_analysis, (sc,))


def time_to_seconds(hours, minutes, seconds):
    return hours * 60 * 60 + minutes * 60 + seconds


s.enter(0, 1, perform_tweet_analysis, (s,))
s.run()

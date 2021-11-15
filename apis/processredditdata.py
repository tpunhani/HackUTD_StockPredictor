from os import replace
from typing import final
from flask import Flask, request, json
from bson.objectid import ObjectId
from numpy import average
import praw

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import pandas as pd 
import re
from sqlalchemy import create_engine
from processvolumedata import fetch_data
import processvolumedata
import mysql.connector

engine = create_engine('mysql+pymysql://root:root@localhost/reddit_data')
analyzer = SentimentIntensityAnalyzer()


#connect to a mysql server 
mydb = mysql.connector.connect(
host ="localhost",
user ="root",
passwd = "root"
)

mycursor = mydb.cursor()

# Create a database for storing reddit data 
mycursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

# Title and body would be used for the sentiment analysis and for counting the number of times a particular ticker is mentioned 
mycursor.execute("""CREATE TABLE IF NOT EXISTS reddit_data.mostmentioned (Term VARCHAR(500),
                Company_Name VARCHAR(500),
                Frequency VARCHAR(50),
                Sentiment VARCHAR(500),
                VolumeMetric VARCHAR(500),
                PriceMetric VARCHAR(500)
                )
                """)

#Initialize reddit api here 
reddit = praw.Reddit(
     client_id="h1ifq1xECRglUV7JuKRHUw",
     client_secret="JZgk3JSuMOByf4M12HYlG7nGMk8jvQ",
     user_agent="Chrome"
 )
print(reddit.read_only)



def process_data():
    df = []
    for post in reddit.subreddit('wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading').hot(limit=500):
        vs = analyzer.polarity_scores(unidecode(post.title + post.selftext))
        sentiment = vs['compound']
        content = {
            "title" : post.title,
            "text" : post.selftext,
            "score": sentiment
        }
        df.append(content)
    df = pd.DataFrame(df)
    regex = re.compile('[^a-zA-Z ]')
    word_dict = {}
    for (index, row) in df.iterrows():
        # titles
        title = row['title']
        title = regex.sub('', title)
        title_words = title.split(' ')
        # content
        content = row['text']
        content = regex.sub('', content)
        content_words = content.split(' ')
        # combine
        words = title_words + content_words
        sent = row['score']
        for x in words:
            if x in ['A', 'B', 'GO', 'ARE', 'ON']:
                pass
            
            elif x in word_dict:
                word_dict[x][0] += 1
                word_dict[x][1].append(sent)
            else:
                word_dict[x] = [1, [sent]]

    final_list = []
    tick = pd.read_csv('ticker.csv')
    for key, value in word_dict.items():
        if key in list(tick['Symbol']):
            volume_data = fetch_data(key)
            final_list.append((key, str(value[0]), average(value[1]), volume_data[0], volume_data[1]))
    
    word_df = pd.DataFrame.from_records(final_list).rename(columns = {0:"Term", 1:"Frequency", 2:"Sentiment", 3:"VolumeMetric", 4:"PriceMetric"})
    # print(word_df)
    ticker_df = pd.read_csv('ticker.csv').rename(columns = {"Symbol":"Term", "Name":"Company_Name"})
    stonks_df = pd.merge(ticker_df, word_df, on="Term")
    stonks_df = stonks_df.sort_values(by=['Frequency'], ascending=False)
    stonks_df.to_sql('mostmentioned', con=engine, if_exists='replace')

process_data()






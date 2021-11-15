
from flask import Flask, jsonify

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost/reddit_data')




app = Flask(__name__)




# Read - list all the items
@app.route("/mostmentioned")
def main():
    data = engine.execute("SELECT * FROM mostmentioned").fetchall()
    return jsonify({'result': [dict(row) for row in data]})


# Read - list top items based on count
@app.route("/mostmentioned/<count>")
def most_count(count):
    data = engine.execute("SELECT * FROM mostmentioned").fetchall()
    data = sorted(data, key=lambda x:int(x[3]), reverse=True)
    return jsonify({'result': [dict(data[i]) for i in range(int(count))]})


# Read - list top items based on sentiment
@app.route("/mostsentimental/<count>")
def most_sentimental(count):
    data = engine.execute("SELECT * FROM mostmentioned").fetchall()
    data = sorted(data, key=lambda x:float(x[4]), reverse=True)
    return jsonify({'result': [dict(data[i]) for i in range(int(count))]})
    



if __name__ == "__main__":
    app.run()   





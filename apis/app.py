
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
    

# Read - get video from Id
# @app.route("/videos/<id>")
# def showVideo(id):
#     record = mycol.find_one({ '_id': ObjectId(id) })
#     record['_id'] = str(record['_id'])
#     return json.dumps(record)




# # Create - Add a new video
# @app.route("/videos", methods=['POST'])
# def newVideo():

#     title = request.args.get('title')
#     desc = request.args.get('desc')

#     new = { "title": title, "description": desc }

#     _id = mycol.insert_one(new)

#     return json.dumps({ 'message': 'Video created successfully! '})


# # Update - update an existing video
# @app.route('/videos/<id>', methods=['PUT'])
# def updateVideo(id):

#     title = request.args.get('title')
#     desc = request.args.get('desc')

#     query = { '_id': ObjectId(id) }

#     newValues = { "$set" : { 'title': title, 'description': desc }}
#     mycol.update_one(query, newValues)

#     return json.dumps({ 'message': 'Video updated successfully' })

# # Delete - delete a video
# @app.route('/videos/<id>', methods=['DELETE'])
# def deleteVideo(id):

#     query = { '_id': ObjectId(id) }
#     mycol.delete_one(query)

#     return json.dumps({ 'message': 'Video deleted successfully '})



if __name__ == "__main__":
    app.run()   





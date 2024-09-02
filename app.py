import pymongo
from flask import Flask

app = Flask(__name__)
mongo = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo['contact']


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)

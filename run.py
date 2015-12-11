#!bin/python
from flask import Flask
import sqlite3

# configuration
DATABASE = 'services.db'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route("/")
def serve_address():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

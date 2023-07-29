#!/usr/bin/python3
""" Entry point to the Flask application
"""
from models import storage
from polls import polls_views
from flask import Flask


app = Flask(__name__)
app.register_blueprint(polls_views)


@app.teardown_appcontext
def close_db(error):
	"""Remove the current SQLAlchemy Session
	"""
	storage.close()


if __name__ == '__main__':
	"""Main Function """
	app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
"""Views for polls
"""
from polls import polls_views
from models import storage
from models.question import Question
from models.choice import Choice
from flask import render_template


@polls_views.route('/', strict_slashes=False)
def index():
	"""Index page
	"""
	return render_template('polls/index.html')

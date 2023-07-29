#!/usr/bin/python3
"""Blueprint (urlpatterns) for API"""
from flask import Blueprint


polls_views = Blueprint('polls_views', __name__, url_prefix='/polls')

from polls.views import *

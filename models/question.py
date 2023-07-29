#!/usr/bin/python3
""" Contains definition of User Model.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage_t


class Question(BaseModel, Base):
	""" The Question class
	"""
	if storage_t == 'db':
		__tablename__ = 'questions'
		question_text = Column(String(200))
		choices = relationship('Choice', backref='questions', cascade='all, delete, delete-orphan')
	else:
		question_text = ''

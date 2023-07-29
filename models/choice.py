#!/usr/bin/python3
""" Contains definition of Choice Model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import BaseModel, Base
from models import storage_t


class Choice(BaseModel, Base):
	""" The Choice class
	"""
	if storage_t == 'db':
		__tablename__ = 'choices'
		choice_text = Column(String(200))
		votes = Column(Integer, nullable=False,  default=0)
		question_id = Column(String(60), ForeignKey('questions.id'), nullable=False) 
	else:
		choice_text = ''
		votes = 0
		question_id = ''



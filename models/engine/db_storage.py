#!/usr/bin/python3
"""Contains the definition of DBStorage
"""
from models.base_model import Base
from models.question import Question
from models.choice import Choice
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {'Question': Question, 'Choice': Choice }


class DBStorage:
	"""
	"""
	__engine = None
	__session = None


	def __init__(self):
		"""Instantiate a DBStorage object"""
		from os import getenv

		PS_MYSQL_USER = getenv('PS_MYSQL_USER')
		PS_MYSQL_PWD = getenv('PS_MYSQL_PWD')
		PS_MYSQL_HOST = getenv('PS_MYSQL_HOST')
		PS_MYSQL_DB = getenv('PS_MYSQL_DB')
		PS_ENV = getenv('PS_ENV')
		self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
									  format(PS_MYSQL_USER,
											 PS_MYSQL_PWD,
											 PS_MYSQL_HOST,
											 PS_MYSQL_DB), pool_pre_ping=True)
		if PS_ENV == "test":
			Base.metadata.drop_all(self.__engine)

	def all(self, cls=None):
		"""query on the current database session"""
		new_dict = {}
		for clss in classes:
			if cls is None or cls is classes[clss] or cls is clss:
				objs = self.__session.query(classes[clss]).all()
				for obj in objs:
					key = obj.__class__.__name__ + '.' + obj.id
					new_dict[key] = obj
		return (new_dict)

	def new(self, obj):
		"""add the object to the current database session"""
		self.__session.add(obj)

	def save(self):
		"""commit all changes of the current database session"""
		self.__session.commit()

	def delete(self, obj=None):
		"""delete from the current database session obj if not None"""
		if obj is not None:
			self.__session.delete(obj)

	def reload(self):
		"""reloads data from the database"""
		Base.metadata.create_all(self.__engine)
		sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
		Session = scoped_session(sess_factory)
		self.__session = Session\
		# self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

	def close(self):
		"""call remove() method on the private session attribute"""
		self.__session.remove()


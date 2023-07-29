#!/usr/bin/python3
""" Contains definition of BaseModel
"""
import uuid
from datetime import datetime
from models import storage_t
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

fmt = "%Y-%m-%dT%H:%M:%S.%f"

if storage_t == 'db':
	Base = declarative_base()
else:
	Base = object


class BaseModel:
	""" Base model class to hold lifecycle functionality for all models. 
	"""
	if storage_t == 'db':
		id = Column(String(60), primary_key=True)
		created_at = Column(DateTime, default=datetime.utcnow())
		updated_at = Column(DateTime, default=datetime.utcnow())

	def __init__(self, *args, **kwargs):
		""" Initialize a new BaseModel Object
		"""
		if not kwargs:
			from models import storage
			self.id = str(uuid.uuid4())
			self.created_at = self.updated_at = datetime.now()
			if storage_t != 'db':
				storage.new(self)
			
		else:
			if kwargs.get('created_at', None): # Existing instance
				kwargs['created_at'] = datetime.strptime(kwargs['created_at'], fmt)
			else:
				kwargs['created_at'] = datetime.utcnow() # New instance from dic
				
			if kwargs.get('updated_at', None): # Existing instance
				kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], fmt)
			else:
				kwargs['updated_at'] = datetime.utcnow() # New instance from dic

			if kwargs.get('__class__', None):
				del kwargs['__class__']
			self.__dict__.update(kwargs)
			
			if kwargs.get('id', None) is None: # New instance from dic
				from models import storage
				self.id = str(uuid.uuid4())
				if storage_t != 'db':
					storage.new(self)


	def __str__(self):
		""" Get string representation of object
		"""
		class_name = self.__class__.__name__
		return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

	def save(self):
		""" Save Changes to Object in storage
		"""
		from models import storage, storage_t
		self.updated_at = datetime.now()
		if storage_t == 'db':
			storage.new(self)
		storage.save()

		
	def to_dict(self):
		""" Get key value store of all atribute is object
		"""
		dic = self.__dict__.copy()
		dic.update({'__class__': self.__class__.__name__})
		dic['created_at'] = self.created_at.isoformat()
		dic['updated_at'] = self.updated_at.isoformat()
		if '_sa_instance_state' in dic:
			del dic['_sa_instance_state']
		return dic

	def delete(self):
		""" Delete the current instance(self) from storage
		"""
		from models import storage
		storage.delete(self)

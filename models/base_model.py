#!/usr/bin/python3
"""
"""
import uuid
from datetime import datetime

fmt = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
	"""
	"""
	def __init__(self, *args, **kwargs):
		""" Initialize a new BaseModel Object
		"""
		if not kwargs:
			from models import storage
			self.id = str(uuid.uuid4())
			self.created_at = self.created_at = datetime.now()
			storage.new(self)
			
		else:
			kwargs['created_at'] = strptime(kwargs['created_at'], fmt)
			kwargs['updated_at'] = strptime(kwargs['updated_at'], fmt)

			del kwargs['__class__']
			self.__dict__.update(kwargs)

	def __str__(self):
		""" Get string representation of object
		"""
		class_name = self.__class__.__name__
		return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

	def save(self):
		""" Save Changes to Object in storage
		"""
		self.updated_at = datetime.now()
		models.storage.save(self)

		
	def to_dict(self):
		""" Get key value store of all atribute is object
		"""
		dic = self.__dict__.copy()
		dic.update({'__class__': self.__class__.__name__})
		dic['created_at'] = self.created_at.isoformat()
		dic['updated_at'] = self.updated_at.isoformat()
		return dic

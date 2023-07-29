#!/usr/bin/python3
""" Contains the definition of FileStorage.
"""

from models.base_model import BaseModel
from models.question import Question
from models.choice import Choice

classes = { 'BaseModel': BaseModel, 'Question': Question, 'Choice': Choice }


class FileStorage:
	"""
	"""
	# path to the JSON file
	__file_path = "dump.json"
	# dictionary to hold all objects
	__objects = {}

	def _all_to_dict(self):
		"""Convert all classes in __objects to dict in readiness
		for serialization
		"""
		temp = {}
		temp.update(FileStorage.__objects)
		
		for key, val in temp.items():
			temp[key] = val.to_dict()

		return temp

	def all(self, cls=None):
		"""Returns all objects of a class if class is given;
		otherwise all objects
		"""
		if cls:
			objs = {k: v for k, v in FileStorage.__objects.items() if type(v) == cls }
			return objs
		else:
			return FileStorage.__objects

	def new(self, obj):
		"""sets in __objects the obj with the key <obj class name>.id
		"""
		key = '{}.{}'.format(obj.__class__.__name__, obj.id) 
		FileStorage.__objects[key] = obj


	def save(self):
		""" Serialize __objects to JSON file
		"""
		import json
		
		with open(FileStorage.__file_path, 'w', encoding='utf-8') as store:
			json_obj = self._all_to_dict()
			json.dump(json_obj, store)


	def reload(self):
		""" Deserialize JSON file to __objects
		"""
		import json

		try:
			with open(FileStorage.__file_path, 'r') as store:
				json_obj = json.load(store)
				
			for k, v in json_obj.items(): 
				FileStorage.__objects[k] = classes[v['__class__']](**v)

		except FileNotFoundError: # Catch where file not found don't create
			pass


	def delete(self, obj=None):
		"""Delete obj from __objects if it's inside
		"""
		if obj:
			key = '{}.{}'.format(obj.__class__.__name__, obj.id)
			if key in FileStorage.__objects:
				del FileStorage.__objects[key]

#!/usr/bin/python3
"""
Module for the entry point of the command interpreter
"""
import cmd
import sys
import shlex
import readline
from models import storage
from models.base_model import BaseModel
from models.question import Question
from models.choice import Choice


class PollsterCommand(cmd.Cmd):
	"""
	Pollster processor definition for Pollster project
	"""

	prompt = '(Pollster) ' if sys.__stdin__.isatty() else ''

	classes = {
		"BaseModel": BaseModel, "Question": Question, "Choice": Choice
	}

	dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

	types = {
		'number_rooms': int, 'number_bathrooms': int,
		'max_guest': int, 'price_by_night': int,
		'latitude': float, 'longitude': float
	}

	def preloop(self):
		"""Prints if isatty is false"""
		if not sys.__stdin__.isatty():
			print('(hbnb)')

	def precmd(self, line):
		"""Reformat command line for advanced command syntax.
		Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
		(Brackets denote optional fields in usage example.)
		"""
		_cmd = _cls = _id = _args = ''  # initialize line elements

		# scan for general formating - i.e '.', '(', ')'
		if not ('.' in line and '(' in line and ')' in line):
			return line

		try:  # parse line left to right
			pline = line[:]  # parsed line

			# isolate <class name>
			_cls = pline[:pline.find('.')]

			# isolate and validate <command>
			_cmd = pline[pline.find('.') + 1:pline.find('(')]
			if _cmd not in PollsterCommand.dot_cmds:
				raise Exception

			# if parantheses contain arguments, parse them
			pline = pline[pline.find('(') + 1:pline.find(')')]
			if pline:
				# partition args: (<id>, [<delim>], [<*args>])
				pline = pline.partition(', ')  # pline convert to tuple

				# isolate _id, stripping quotes
				_id = pline[0].replace('\"', '')
				# possible bug here:
				# empty quotes register as empty _id when replaced

				# if arguments exist beyond _id
				pline = pline[2].strip()  # pline is now str
				if pline:
					# check for *args or **kwargs
					if pline[0] == '{' and pline[-1] == '}'\
							and type(eval(pline)) is dict:
						_args = pline
					else:
						_args = pline.replace(',', '')
						# _args = _args.replace('\"', '')
			line = ' '.join([_cmd, _cls, _id, _args])


		except Exception as mess:
			pass
		finally:
			return line

	def postcmd(self, stop, line):
		"""Prints if isatty is false"""
		if not sys.__stdin__.isatty():
			print('(hbnb) ', end='')
		return stop

	def do_quit(self, line):
		"""
		Quit command to exit the program
		"""
		exit()

	def do_EOF(self, line):
		"""
		EOF command to exit the program
		"""
		print()
		exit()

	def emptyline(self):
		""" Overrides the emptyline method of CMD"""
		pass

	def _key_value_parser(self, args):
		"""creates a dictionary from a list of strings"""
		new_dict = {}
		for arg in args:
			if "=" in arg:
				kvp = arg.split('=', 1)
				key = kvp[0]
				value = kvp[1]
				if value[0] == value[-1] == '"':
					value = shlex.split(value)[0].replace('_', ' ')
				else:
					try:
						value = int(value)
					except BaseException:
						try:
							value = float(value)
						except BaseException:
							continue
				new_dict[key] = value
		return new_dict

	def do_create(self, arg):
		"""
		Creates a new instance of BaseModel, saves it
		(to the JSON file) and prints the id.
		Ex1: $ create BaseModel

		Ex2: $ create <Class name> <param 1>  <param 2> <param 3>...
		Ex2: $ create State name="California"
		"""
		args = arg.split()
		if len(args) == 0:
			print("** class name missing **")
			return False
		if args[0] in PollsterCommand.classes:
			new_dict = self._key_value_parser(args[1:])
			try:
				instance = PollsterCommand.classes[args[0]](**new_dict)
			except:
				print("** invalid or not enough arguments **")
		else:
			print("** class doesn't exist **")
			return False
		print(instance.id)
		instance.save()

	def do_show(self, args):
		"""
		Prints the string representation of an instance
		based on the class name and id.
		Ex1: $ show BaseModel 1234-1234-1234.

		Ex2: $ <class name>.show(<id>) e.g. User.show('246c227a-d...')
		"""
		new = args.partition(" ")
		c_name = new[0]
		c_id = new[2]

		# guard against trailing args
		if c_id and ' ' in c_id:
			c_id = c_id.partition(' ')[0]

		if not c_name:
			print("** class name missing **")
			return

		if c_name not in PollsterCommand.classes:
			print("** class doesn't exist **")
			return

		if not c_id:
			print("** instance id missing **")
			return

		key = c_name + "." + c_id
		try:
			print(storage._FileStorage__objects[key])
		except KeyError:
			print("** no instance found **")

	def do_destroy(self, args):
		"""
		Deletes an instance based on the class name
		and id (save the change into the JSON file).
		Ex1: $ destroy BaseModel 1234-1234-1234

		Ex2: $ <class name>.destroy(<id>) e.g. User.destroy('3jdjd-d...')
		"""
		new = args.partition(" ")
		c_name = new[0]
		c_id = new[2]
		if c_id and ' ' in c_id:
			c_id = c_id.partition(' ')[0]

		if not c_name:
			print("** class name missing **")
			return

		if c_name not in PollsterCommand.classes:
			print("** class doesn't exist **")
			return

		if not c_id:
			print("** instance id missing **")
			return

		key = c_name + "." + c_id

		try:
			del (storage.all()[key])
			storage.save()
		except KeyError:
			print("** no instance found **")

	def do_all(self, args):
		"""
		Prints all string representation of all instances
		based or not on the class name.
		Ex1: $ all BaseModel or $ all

		Ex2: $ <class name>.all() e.g. $ User.all()
		"""
		print_list = []

		if args:
			args = args.split(' ')[0]  # remove possible trailing args
			if args not in PollsterCommand.classes:
				print("** class doesn't exist **")
				return
			for k, v in storage.all().items():
				if k.split('.')[0] == args:
					print_list.append(str(v))
		else:
			for k, v in storage.all().items():
				print_list.append(str(v))

		print(print_list)

	def do_count(self, args):
		"""
		Count current number of class instances
		Ex1: $ count BaseModel

		Ex2: $ <class name>.count() e.g. User.count()
		"""
		count = 0
		for k, v in storage.all().items():
			if args == k.split('.')[0]:
				count += 1
		print(count)

	def do_update(self, arg):
		"""
		Updates an instance based on the class name and
		id by adding or updating attribute (save the change
		into the JSON file).
		Ex1: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"

		Ex2: $ <class name>.update(<id>, <attribute name>, <attribute value>)
		Ex2: $ User.update('sfsah3-d3343...', 'first_name', 'John')

		Ex3: $ <class name>.update(<id>, <dictionary representation>)
		Ex3: $ User.update('ddafj3-d...', {'first_name': John, 'age': 89})
		"""
		args = shlex.split(arg)
		integers = ['votes']
		floats = []
		if len(args) == 0:
			print("** class name missing **")
		elif args[0] in PollsterCommand.classes:
			if len(args) > 1:
				k = args[0] + "." + args[1]
				if k in storage.all():
					if len(args) > 2:
						if len(args) > 3:
							if args[0] == "Place":
								if args[2] in integers:
									try:
										args[3] = int(args[3])
									except:
										args[3] = 0
								elif args[2] in floats:
									try:
										args[3] = float(args[3])
									except:
										args[3] = 0.0
							setattr(storage.all()[k], args[2], args[3])
							storage.all()[k].save()
						else:
							print("** value missing **")
					else:
						print("** attribute name missing **")
				else:
					print("** no instance found **")
			else:
				print("** instance id missing **")
		else:
			print("** class doesn't exist **")


if __name__ == '__main__':
	PollsterCommand().cmdloop()


import exceptions


class FCDevice(object):
	""" Abstract class representing a field controller device. """
	
	def __init__(self):
		pass

	def add_object(self, device):
		raise exceptions.NotImplementedError()

	def iter_objects(self):
		raise exceptions.NotImplementedError()

	@property
	def num_objects(self):
		raise exceptions.NotImplementedError()

	@property
	def objects(self):
		raise exceptions.NotImplementedError()
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

	@property
	def pin(self):
	    return self.get_pin()
	@pin.setter
	def pin(self, newpin):
		return self.set_pin(newpin)

	def get_pin(self):
		raise NotImplementedError()

	def set_pin(self, newpin):
		raise NotImplementedError()

	@property
	def datetime(self):
	    return self.get_datetime()

	def get_datetime(self):
		raise NotImplementedError()
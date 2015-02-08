from hmi.FCDevice import FCDevice


class MockFCDevice(FCDevice):
	""" Mock field controller device to be used for testing purposes. """
	
	def __init__(self):
		super(MockFCDevice, self).__init__()
		self._objects = {}

	def add_object(self, obj):
		self._objects[obj.id] = obj

	def iter_objects(self):
		return iter(self._objects.values())

	@property
	def num_objects(self):
		return len(self._objects)

	@property
	def objects(self):
		return self._objects
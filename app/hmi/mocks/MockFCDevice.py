from hmi.FCDevice import FCDevice
import time

class MockFCDevice(FCDevice):
	""" Mock field controller device to be used for testing purposes. """
	
	def __init__(self):
		super(MockFCDevice, self).__init__()
		self._objects = {}
		self._pin = 123456

	def add_object(self, obj):
		self._objects[obj.objinst] = obj

	def iter_objects(self):
		return iter(self.objects.values())

	@property
	def num_objects(self):
		return len(self.objects)

	@property
	def objects(self):
		return self._objects

	def get_pin(self):
		return self._pin

	def set_pin(self, newpin):
		self._pin = newpin

	def get_datetime(self):
		return int(time.time())
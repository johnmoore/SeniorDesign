from hmi.FCObject import FCObject 
import exceptions
import random
import time


class MockFCObject(FCObject):
	def __init__(self, id, name, value, units, mutable=True):
		self._historic_data = [(time.time(), None)]
		super(MockFCObject, self).__init__(id, name, value, units, mutable)

	def update_value(self, value=None):
		if not self._mutable:
			raise ObjectNotMutableError()
		if not value:
			value = self.value + round(random.random() - 0.5, 1)
		self._historic_data.append((int(time.time()), self.value))
		self.value = value

	def get_historic_data(self, num_samples, interval):
		samples = reversed(self._historic_data)
		current_sample = next(samples)
		current_time = int(time.time())
		data = {}
		i = 0
		while i < num_samples:
			ts, v = current_sample
			if v == None:
				break
			if ts <= current_time:
				data[i] = v
				current_time -= interval
				i += 1
			else:
				current_sample = next(samples)
		while i < num_samples:
			data[i] = None
			i += 1
		return data
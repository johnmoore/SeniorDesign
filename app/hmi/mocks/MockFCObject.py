from hmi.FCObject import FCObject 
import exceptions
import random
import time


class MockFCObject(FCObject):
	def __init__(self, objtype, objinst, name=None, value=None, units=None, mutable=True):
		self._historic_data = [(time.time(), value)]
		super(MockFCObject, self).__init__(objtype, objinst, name, value, units, mutable)
		self.value = value

	def get_historic_data(self, num_samples, interval):
		print self._historic_data
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
				try:
					current_sample = next(samples)
				except Exception:
					break
		while i < num_samples:
			data[i] = None
			i += 1
		return data

	def get_value(self):
		return self._value

	def set_value(self, value):
		if not self._mutable:
			raise ObjectNotMutableError()
		if not value:
			value = self.value + round(random.random() - 0.5, 1)
		self._value = value
		self._historic_data.append((int(time.time()), self.value))
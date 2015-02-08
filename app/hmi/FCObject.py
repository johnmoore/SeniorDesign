import exceptions


class FCObject(object):
	def __init__(self, id, name, value, units, mutable=True):
		self.id = id
		self.name = name
		self.units = units
		self.value = value
		self._mutable = mutable
		self.update_value(value)

	def __iter__(self):
		return self._output()

	def _output(self):
		yield ('id', self.id)
		yield ('name', self.name)
		yield ('value', self.value)
		yield ('formatted_value', self.formatted_value)
		yield ('units', self.units)

	def update_value(self):
		raise exceptions.NotImplementedError()

	def get_historic_data(self, num_samples, interval):
		raise exceptions.NotImplementedError()

	@property
	def formatted_value(self):
		if self.units:
			return str(self.value) + ' ' + self.units
		else:
			return str(self.value)

	@property
	def value(self):
	    return self._value
	@value.setter
	def value(self, value):
	    self._value = value

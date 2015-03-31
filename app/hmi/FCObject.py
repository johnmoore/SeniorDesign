import exceptions
import time


class FCObject(object):
	def __init__(self, objtype, objinst, name=None, value=None, units=None, historic=False, mutable=True):
		self.objtype = objtype
		self.objinst = objinst
		self.units = units
		self.name = name
		self._mutable = mutable
		self._historic = historic

	def __iter__(self):
		return self._output()

	def _output(self):
		yield ('id', self.id)
		yield ('type', self.objtype)
		yield ('name', ('Object #'+str(self.id) if not self.name else self.name))
		yield ('value', self.value)
		yield ('formatted_value', self.formatted_value)
		yield ('units', ('' if not self.units else self.units))
		yield ('detail', self._mutable)
		yield ('historic', self._historic)

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
	    return self.get_value()
	@value.setter
	def value(self, value):
		return self.set_value(value)

	def get_value(self):
		raise NotImplementedError()

	def set_value(self, value):
		raise NotImplementedError()

	@property
	def id(self):
	    return self.objinst
	
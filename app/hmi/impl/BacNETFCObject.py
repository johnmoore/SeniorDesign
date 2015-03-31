from hmi.FCObject import FCObject 
import exceptions
import random
import time


class BacNETFCObject(FCObject):
	def __init__(self, device, objtype, objinst, name=None, units=None, historic=False, mutable=True):
		#self._historic_data = [(time.time(), None)]
		self._owner = device
		super(BacNETFCObject, self).__init__(objtype, objinst, name, None, units, historic, mutable)
		self._value = None

	def get_value(self):
		self._value = self._owner.read_present_val(self.objtype, self.objinst)
		return self._value

	def set_value(self, value):
		if not self._mutable:
			raise ObjectNotMutableError()
		res = self._owner.write_present_val(self.objtype, self.objinst, value)
		if res:
			self._value = value
		else:
			raise Exception("Error updating value")

	def get_historic_data(self, num_samples, interval):
		entries = range(0, num_samples*interval, interval)
		print entries
		historic_data = self._owner.read_trend_log_entries(self.objinst, entries)
		print historic_data
		data = {}
		i = 0
		while i < num_samples:
			try:
				data[i] = historic_data[i][1]
			except Exception:
				data[i] = None
			i = i + 1
		return data
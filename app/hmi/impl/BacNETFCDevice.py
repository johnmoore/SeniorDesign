from hmi.FCDevice import FCDevice
from hmi.bacnet.HMIBacNETClient import HMIBacNETClient
from hmi.impl.BacNETFCObject import BacNETFCObject
import exceptions
import time
import calendar
import datetime
from datetime import tzinfo, timedelta


class BacNETFCDevice(FCDevice):
	""" Mock field controller device to be used for testing purposes. """
	
	def __init__(self, bacnet_id):
		super(BacNETFCDevice, self).__init__()
		self._objects = {}
		self.device_id = bacnet_id
		self._client = HMIBacNETClient('192.168.2.1', self)
		self._trend_logs = {}

	def initialize(self):
		self._client.connect()

	def _add_object(self, obj):
		self._objects[obj.objinst] = obj

	def iter_objects(self):
		return iter(self.objects.values())

	@property
	def num_objects(self):
		return len(self.objects)

	@property
	def objects(self):
		r = self.read_obj_list()
		seen = []
		for objtype, objinst in r:
			if objinst not in self._objects and objtype in ['analogInput']:
				newobj = BacNETFCObject(self, objtype, objinst, self.read_obj_name(objtype, objinst), self.read_obj_units(objtype, objinst))
				self._add_object(newobj)
			elif objinst not in self._objects and objtype == 'trendLog':
				newobj = BacNETFCObject(self, objtype, objinst)
				target = self.read_trend_log_target(objinst)
				self._trend_logs[target] = newobj
				self._objects[target]._historic = True
			seen.append(objinst)
		for c in self._objects.keys():
			if c not in seen:
				del self._objects[c]
		return self._objects

	@property
	def client(self):
	    return self._client

	def read_present_val(self, objtype, objinst):
		return self._client.read_present_val(objtype, objinst)

	def read_obj_list(self):
		return self._client.read_obj_list()

	def write_present_val(self, objtype, objinst, newval):
		res = self._client.write_present_val(objtype, objinst, newval)
		if not res:
			raise Exception("Unable to write new value")
		return True

	def read_obj_name(self, objtype, objinst):
		return self._client.read_obj_name(objtype, objinst)

	def set_pin(self, newpin):
		res = self._client.write_present_val('analogValue', 7002, float(newpin))
		if not res:
			raise Exception("Unable to set PIN")
		return True

	def get_pin(self):
		return int(self._client.read_present_val('analogValue', 7002))

	def get_datetime(self):
		ddate = self._client.read_date()
		dtime = self._client.read_time()
		ret = datetime.datetime(ddate[0]+1900, ddate[1], ddate[2], dtime[0], dtime[1], dtime[2])
		return str(ret)

	def read_obj_units(self, objtype, objinst):
		ret = self._client.read_obj_units(objtype, objinst)
		if ret == 'degreesFahrenheit':
			return 'F'
		elif ret == 'partsPerMillion':
			return 'PPM'
		elif ret == 'percent':
			return '%'
		elif ret == 'poundsForcePerSquareInch':
			return 'PSI'
		else:
			return ''
		return ret

	def read_trend_log_target(self, objinst):
		res = self._client.read_trend_log_target(objinst)
		res = int(res.objectIdentifier[1])
		return res

	def read_trend_log(self, objinst):
		res = self._client.read_trend_log(self._trend_logs[objinst].objinst)
		return res

	def read_trend_log_entries(self, objinst, entries):
		res = self._client.read_trend_entries(self._trend_logs[objinst].objinst, entries)
		print "res2:" + str(res)
		return res


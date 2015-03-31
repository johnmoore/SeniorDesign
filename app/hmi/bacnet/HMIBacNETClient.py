import sys
import thread
import time

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.consolecmd import ConsoleCmd

from bacpypes.core import run, run_once

from bacpypes.pdu import Address
from bacpypes.app import LocalDeviceObject, BIPSimpleApplication
from bacpypes.object import get_object_class, get_datatype

from bacpypes.apdu import ReadPropertyRequest, Error, AbortPDU, ReadPropertyACK, WritePropertyRequest, SimpleAckPDU, ReadRangeRequest, ReadRangeACK
from bacpypes.primitivedata import Unsigned
from bacpypes.constructeddata import Array

from bacpypes.primitivedata import *
from bacpypes.constructeddata import *
from bacpypes.basetypes import *
import threading
from bacpypes.apdu import RangeByPosition, Range

@bacpypes_debugging
class HMIApplication(BIPSimpleApplication):

	def __init__(self, hmi, *args):
		self._debug = True
		self._hmi = hmi
		if self._debug: print("__init__ %r", args)
		BIPSimpleApplication.__init__(self, *args)
		if self._debug: print("super called")
		# keep track of requests to line up responses
		self._request = None

	def request(self, apdu):
		if self._debug: print("request %r", apdu)

		# save a copy of the request
		self._request = apdu

		# forward it along
		BIPSimpleApplication.request(self, apdu)
		if self._debug: print "ok"

	def confirmation(self, apdu):
		if self._debug: print("confirmation %r", apdu)

		if isinstance(apdu, Error):
			sys.stdout.write("error: %s\n" % (apdu.errorCode,))
			sys.stdout.flush()
			if isinstance(self._request, WritePropertyRequest):
				self._hmi.report(False)
			elif isinstance(self._request, ReadPropertyRequest):
				self._hmi.report(None)

		elif isinstance(apdu, AbortPDU):
			apdu.debug_contents()

		elif (isinstance(self._request, ReadPropertyRequest)) and (isinstance(apdu, ReadPropertyACK)):
			# find the datatype
			datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
			if self._debug: print("	- datatype: %r", datatype)
			if not datatype:
				raise TypeError, "unknown datatype"

			# special case for array parts, others are managed by cast_out
			if issubclass(datatype, Array) and (apdu.propertyArrayIndex is not None):
				if apdu.propertyArrayIndex == 0:
					value = apdu.propertyValue.cast_out(Unsigned)
				else:
					value = apdu.propertyValue.cast_out(datatype.subtype)
			else:
				value = apdu.propertyValue.cast_out(datatype)
				if isinstance(value, float):
					value = round(value, 4)
				self._hmi.report(value)
			if self._debug: print("	- value: %r", value)

			#sys.stdout.write(str(value) + '\n')
			if hasattr(value, 'debug_contents'):
				value.debug_contents(file=sys.stdout)
			sys.stdout.flush()

		elif (isinstance(self._request, WritePropertyRequest)) and (isinstance(apdu, SimpleAckPDU)):
			self._hmi.report(True)

		elif (isinstance(self._request, ReadRangeRequest)) and (isinstance(apdu, ReadRangeACK)):
			# find the datatype
			datatype = get_datatype(apdu.objectIdentifier[0], apdu.propertyIdentifier)
			if self._debug: print("	- datatype: %r", datatype)
			if not datatype:
				raise TypeError, "unknown datatype"

			# cast out of the single Any element into the datatype
			value = apdu.itemData[0].cast_out(datatype)

			# dump it out
			res = []
			for i, item in enumerate(value):
				res.append((i, item.logDatum.realValue))
			self._hmi.report(res)

		
@bacpypes_debugging
class HMIBacNETClient(object):

	def __init__(self, remote_addr, owner, args={'objectname':'HMI',
							 'objectidentifier': 0,
							 'maxapdulengthaccepted': 1024,
							 'segmentationsupported': 'segmented-both',
							 'vendoridentifier': 10,
							 'address': '0.0.0.0'}, debug=True):
		self._args = args
		self._app = None
		self._debug = debug
		self._owner = owner
		self._device = LocalDeviceObject(
				objectName=self._args['objectname'],
				objectIdentifier=int(self._args['objectidentifier']),
				maxApduLengthAccepted=int(self._args['maxapdulengthaccepted']),
				segmentationSupported=self._args['segmentationsupported'],
				vendorIdentifier=int(self._args['vendoridentifier']),
				)
		self._remote_addr = remote_addr
		self._done = True
		self._result = None
		self._lock = threading.Lock()

	def connect(self):
		try:
			# make a simple application
			self._app = HMIApplication(self, self._device, self._args['address'])
			if self._debug: print "connecting"
			#run()
			if self._debug: print "running"
			thread.start_new_thread(run, ())
		except Exception, e:
			print "exception:" + repr(e)

	def _do_read(self, objtype, objinst, propname):

		try:
			addr, obj_type, obj_inst, prop_id = self._remote_addr, objtype, objinst, propname

			if obj_type.isdigit():
				obj_type = int(obj_type)
			elif not get_object_class(obj_type):
				raise ValueError, "unknown object type"

			obj_inst = int(obj_inst)

			datatype = get_datatype(obj_type, prop_id)
			if not datatype:
				raise ValueError, "invalid property for object type"

			# build a request
			request = ReadPropertyRequest(
				objectIdentifier=(obj_type, obj_inst),
				propertyIdentifier=prop_id,
				)
			if self._debug: print("requesting")
			request.pduDestination = Address(addr)

			#if len(args) == 5:
			#	request.propertyArrayIndex = int(args[4])
			#if _debug: ReadPropertyConsoleCmd._debug("	- request: %r", request)

			# give it to the application
			self._app.request(request)

		except Exception, e:
			print "exception:" + repr(e)

	def _do_write(self, objtype, objinst, propname, new_val):
		try:
			addr, obj_type, obj_inst, prop_id = self._remote_addr, objtype, objinst, propname

			if obj_type.isdigit():
				obj_type = int(obj_type)
			elif not get_object_class(obj_type):
				raise ValueError, "unknown object type"

			obj_inst = int(obj_inst)

			datatype = get_datatype(obj_type, prop_id)
			if not datatype:
				raise ValueError, "invalid property for object type"

			print 'new val:' + str(new_val)
			prop_val = Any(Real(float(new_val)))
			#prop_val.cast_in()

			# build a request
			request = WritePropertyRequest(
				objectIdentifier=(obj_type, obj_inst),
				propertyIdentifier=prop_id,
				propertyValue=prop_val
				)
			request.pduDestination = Address(addr)
			if self._debug: print("writing")

			#if len(args) == 5:
			#	request.propertyArrayIndex = int(args[4])
			#if _debug: ReadPropertyConsoleCmd._debug("	- request: %r", request)

			# give it to the application
			self._app.request(request)

		except Exception, e:
			print "exception:" + repr(e)


	def _do_readrange(self, objtype, objinst, propname, start, c, arrind=None):
		try:
			addr, obj_type, obj_inst, prop_id =  self._remote_addr, objtype, objinst, propname

			if obj_type.isdigit():
				obj_type = int(obj_type)
			elif not get_object_class(obj_type):
				raise ValueError, "unknown object type"

			obj_inst = int(obj_inst)

			datatype = get_datatype(obj_type, prop_id)
			if not datatype:
				raise ValueError, "invalid property for object type"

			# build a request
			request = ReadRangeRequest(
				objectIdentifier=(obj_type, obj_inst),
				propertyIdentifier=prop_id,
				range=Range(byPosition=RangeByPosition(referenceIndex=start, count=c))
				)
			request.pduDestination = Address(addr)

			if arrind:
				request.propertyArrayIndex = int(arrind)
			#if _debug: ReadRangeConsoleCmd._debug("	- request: %r", request)

			# give it to the application
			self._app.request(request)

		except Exception, e:
			print "exception:" + repr(e)

	def read_present_val(self, objtype, objinst):
		self._lock.acquire()
		self._done = False
		self._do_read(objtype, objinst, 'presentValue')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def write_present_val(self, objtype, objinst, newval):
		self._lock.acquire()
		self._done = False
		self._do_write(objtype, objinst, 'presentValue', newval)
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_obj_list(self):
		self._lock.acquire()
		self._done = False
		self._do_read('device', self._owner.device_id, 'objectList')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_obj_name(self, objtype, objinst):
		self._lock.acquire()
		self._done = False
		self._do_read(objtype, objinst, 'objectName')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_time(self):
		self._lock.acquire()
		self._done = False
		self._do_read('device', self._owner.device_id, 'localTime')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_date(self):
		self._lock.acquire()
		self._done = False
		self._do_read('device', self._owner.device_id, 'localDate')
		while not self._done:
			pass
		self._lock.release()
		return self._result	

	def read_obj_units(self, objtype, objinst):
		self._lock.acquire()
		self._done = False
		self._do_read(objtype, objinst, 'units')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_trend_log_target(self, objinst):
		self._lock.acquire()
		self._done = False
		self._do_read('trendLog', objinst, 'logDeviceObjectProperty')
		while not self._done:
			pass
		self._lock.release()
		return self._result

	def read_trend_log(self, objinst, maxi=3000):
		self._lock.acquire()
		self._done = False
		self._do_read('trendLog', objinst, 'recordCount')
		while not self._done:
			pass
		self._lock.release()
		entries = int(self._result)
		maxi = min(maxi, entries)

		if maxi <= 19:
			self._lock.acquire()
			self._done = False
			self._do_readrange('trendLog', objinst, 'logBuffer', 1, maxi)
			while not self._done:
				pass
			self._lock.release()
			return self._result
		i = 1
		results = []
		while i <= maxi:
			endi = min(i+18, maxi)
			self._lock.acquire()
			self._done = False
			self._do_readrange('trendLog', objinst, 'logBuffer', i, endi)
			while not self._done:
				pass
			self._lock.release()
			res = self._result
			for ci, v in res:
				results.append((i+ci, v))
			i = i + 19
		return results

	def read_trend_entries(self, objinst, entries):
		self._lock.acquire()
		self._done = False
		self._do_read('trendLog', objinst, 'recordCount')
		while not self._done:
			pass
		self._lock.release()
		nentries = int(self._result)
		maxi = nentries

		results = []
		print "entries:" + str(entries)
		for entry in entries:
			if entry <= maxi and nentries-entry >= 1:
				self._lock.acquire()
				self._done = False
				self._do_readrange('trendLog', objinst, 'logBuffer', nentries-entry, 1)
				while not self._done:
					pass
				self._lock.release()
				print "res3:" + str(self._result)
				results.append((entry, self._result[0][1]))
		
		return results


	def report(self, val):
		self._result = val
		self._done = True


"""
if __name__ == "__main__":
	print "running"

	hmi = HMIBacNETClient('10.211.55.4')
	hmi.connect(
	time.sleep(5)
	#run_once()
	print 'result:' + str(hmi.read_present_val('analogValue', '201'))
	#run_once
	print 'result:' + str(hmi.read_present_val('analogValue', '201'))
	#run_once
	print 'result:' + str(hmi.read_present_val('analogValue', '201'))
	#run_once()
	time.sleep(5)
"""

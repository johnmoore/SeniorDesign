import urllib
import urllib2
import time
from hmi.mocks.MockFCObject import MockFCObject
from hmi.tests.HMITest import HMITest
import json
import random

class FCIntegrationTest(object):
	def _update_sensor(self, id, val):
		try:
			url = 'http://hmi:5000/objects/update/'
			values = {'id' : id, 'val': val}
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
		except Exception:
			return False
		return True

	def _get_object_list(self):
		try:
			url = 'http://hmi:5000/objects/list/'
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
		except Exception:
			return False
		return json.loads(response.read())

	def run_test(self):
		objects = self._get_object_list()

		# set initial values
		for obj in objects['data']:
				print obj
				val = float(obj['value'])
				if obj['units'] == 'F':
					delta = 1
					initial = 72 + round(random.random() * delta - delta/2, 1)
				elif obj['units'] == 'PPM':
					delta = 100
					initial = 1000 + round(random.random() * delta - delta/2, 1)
				elif obj['units'] == '%':
					delta = 10
					initial = 20 + round(random.random() * delta - delta/2, 1)
				elif obj['units'] == 'PSI':
					delta = 3
					initial = 40 + round(random.random() * delta - delta/2, 1)
				val = initial
				print str(time.time()) + "] Setting sensor '" + obj['name'] + "' to initial value of " + str(val)
				self._update_sensor(int(obj['id']), val)

		while (True):
			objects = self._get_object_list()
			for obj in objects['data']:
				print obj
				val = float(obj['value'])
				print 'current:' + str(val)
				if obj['units'] == 'F':
					delta = 1
				elif obj['units'] == 'PPM':
					delta = 10
				elif obj['units'] == '%':
					delta = 1
				elif obj['units'] == 'PSI':
					delta = 0.5
				d = str(round(random.random() * delta - delta/2.0, 1))
				print 'to add:' + str(d)
				val = val + round(random.random() * delta - delta/2.0, 1)
				print 'now: ' + str(val)
				print str(time.time()) + "] Updating sensor '" + obj['name'] + "' to new value of " + str(val)
				self._update_sensor(int(obj['id']), val)
			time.sleep(2)

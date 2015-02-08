import urllib
import urllib2
import time
from hmi.mocks.MockFCObject import MockFCObject
from hmi.tests.HMITest import HMITest


class FCIntegrationTest(HMITest):
	def _update_sensor(self, id, val):
		try:
			url = 'http://127.0.0.1:5000/objects/update/'
			values = {'id' : id, 'val': val}
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
		except Exception:
			return False
		return True


	def run_test(self):
		objects = [MockFCObject(0, 'Rm 113 Temperature', 72.1, 'F'), MockFCObject(1, 'Rm 113 Humidity', 20.5, '%')]

		while (True):
			for id, obj in enumerate(objects):
				obj.update_value()
				val = obj.value
				print str(time.time()) + "] Updating sensor '" + obj.name + "' to new value of " + str(val)
				self._update_sensor(id, val)
			time.sleep(2)
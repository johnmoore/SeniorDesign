import urllib
import urllib2
import time
from hmi.tests.HMITest import HMITest


class FCObjAddTest(HMITest):
	def _add_sensor(self):
		try:
			url = 'http://128.197.180.170:5000/objects/add/'
			values = {'name':'Fire Alarm System', 'value':'OK'}
			print "Adding sensor: " + str(values)
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
		except Exception:
			return False
		return True


	def run_test(self):
		self._add_sensor()
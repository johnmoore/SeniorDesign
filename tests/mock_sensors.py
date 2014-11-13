import random
import urllib
import urllib2
import time

def UpdateSensor(sid, val):
	url = 'http://128.197.180.250:5000/sensors/update/'
	values = {'sid' : sid, 'val': val}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	return True

random.seed()

class Sensor(object):
	def __init__(self, name, value, units):
		self.sname = name
		self._svalue = value
		self.units = units
		self.n = 0

	def UpdateValue(self):
		pass

	@property
	def svalue(self):
		self.UpdateValue()
		return self._svalue
	


class MockSensor(Sensor):
	def __init__(self, name, value, units):
		super(MockSensor, self).__init__(name, value, units)

	def UpdateValue(self):
		self._svalue += round(random.random() - 0.5, 1)


sensors = [MockSensor('Rm 113 Temperature', 72.1, 'F'), MockSensor('Rm 113 Humidity', 20.5, '%')]


while (True):
	for sid, sensor in enumerate(sensors):
		sval = sensor.svalue
		print "Updating sensor '" + sensor.sname + "' to new value of " + str(sval)
		UpdateSensor(sid, sval)
	time.sleep(1)



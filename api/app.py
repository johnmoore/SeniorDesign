#!/home/debian/SeniorDesign/api/flask/bin/python
from flask import Flask, jsonify
from flask import make_response, request, current_app
from functools import update_wrapper
import random


app = Flask(__name__)

random.seed()

def crossdomain(origin=None):
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            h['Pragma'] = 'no-cache'
            h['Expires'] = '0'
	    return resp
        return update_wrapper(wrapped_function, f)
    return decorator


class Sensor(object):
	def __init__(self, name, value, units):
		self.sname = name
		self.svalue = value
		self.units = units
		self.n = 0

	def __iter__(self):
		return self

	def UpdateValue(self):
		pass

	def next(self):
		if self.n == 0:
			self.n += 1
			return ('sname', self.sname)
		elif self.n == 1:
			self.n += 1
			if self.units:
				return ('svalue', str(self.svalue) + ' ' + self.units)
			else:
				return ('svalue', str(self.svalue))
		else:
			self.n = 0
			self.UpdateValue()
			raise StopIteration


class MockSensor(Sensor):
	def __init__(self, name, value, units):
		super(MockSensor, self).__init__(name, value, units)

	def UpdateValue(self):
		self.svalue += round(random.random() - 0.5, 1)


sensors = [Sensor('Rm 113 Temperature', 72.1, 'F'), Sensor('Rm 113 Humidity', 20.5, '%'), Sensor('Rm 113 Lighting', 80, '%'), Sensor('HVAC Fan Speed', 'LO', None), Sensor('Fire Alarm System', 'OK', None)]


@app.route('/sensors/list/', methods=['GET'])
@crossdomain(origin='*')
def list_sensors():
	return jsonify({'total': len(sensors), 'data': [dict(sensor) for sensor in sensors]})

@app.route('/sensors/update/', methods=['POST'])
@crossdomain(origin='*')
def update_sensor():
	sid = 2
	if 'val' not in request.form:
		return jsonify({'status': 'err'})
	if 'sid' in request.form:
		sid = int(request.form['sid'])
	if sid == 2:
		newval = int(request.form['val'])
	else:
		newval = float(request.form['val'])
	sensors[sid].svalue = newval
	return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')


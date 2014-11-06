#!flask/bin/python
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
	def __init__(self, name, value):
		self.sname = name
		self.svalue = value
		self.n = 0

	def __iter__(self):
		return self

	def next(self):
		if self.n == 0:
			self.n += 1
			return ('sname', self.sname)
		elif self.n == 1:
			self.n += 1
			return ('svalue', self.svalue)
		else:
			self.n = 0
			raise StopIteration


@app.route('/sensors/list/', methods=['GET'])
@crossdomain(origin='*')
def list_sensors():
	sensors = [Sensor('Temperature', str(random.randint(45,80)) + 'F'), Sensor('Humidity', str(random.randint(45,80)) + '%')]
	return jsonify({'total': len(sensors), 'data': [dict(sensor) for sensor in sensors]})

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')


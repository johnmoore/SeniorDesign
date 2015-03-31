#!/hmi/api/flask/bin/python
from hmi import app
from hmi import util
from hmi import exceptions
import logging
import random
import sys
from flask import make_response

app.DEVICE = None

@app.errorhandler(500)
def handle_err(error):
	response = make_response("Error: " + repr(error), 500)
	return response

def start_app(debug=True):
	logging.debug('Starting app in ' + ('debug' if debug else 'production') + ' mode')
	if debug == True:
		random.seed()
		app.DEVICE = util.init_debug_device()
		app.DEVICE.pin = 123456
	else:
		random.seed()
		app.DEVICE = util.init_hmi_device()
		pass
	app.run(debug=debug, threaded=True, host='0.0.0.0')


if __name__ == '__main__':
	debug = False
	if len(sys.argv) < 2 or sys.argv[1] == 'debug':
		debug = True
	start_app(debug)

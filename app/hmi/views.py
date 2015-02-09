from flask import jsonify
from flask import make_response, request
from hmi import app
import exceptions
import util


@app.route('/objects/list/', methods=['GET'])
@util.crossdomain(origin='*')
def list_objects():
	return make_response(
		jsonify({'total': app.DEVICE.num_objects, 
				 'data': [dict(obj) for obj in app.DEVICE.iter_objects()]}), 200)


@app.route('/objects/update/', methods=['POST'])
@util.crossdomain(origin='*')
def update_objects():
	if 'val' not in request.form:
		raise exceptions.InvalidRequestError()
	if 'id' not in request.form:
		raise exceptions.InvalidRequestError()
	id = int(request.form['id'])
	newval = float(request.form['val'])
	app.DEVICE.objects[id].update_value(newval)
	return util.Success()


@app.route('/objects/get/', methods=['GET'])
@util.crossdomain(origin='*')
def get_object():
	if 'id' not in request.args:
		raise exceptions.InvalidRequestError()
	id = int(request.args['id'])
	try:
		val = dict(app.DEVICE.objects[id])
	except KeyError:
		raise exceptions.ObjectDoesNotExistError()
	return make_response(jsonify({'value': val}), 200)


@app.route('/objects/get/historic/', methods=['GET'])
@util.crossdomain(origin='*')
def get_historic_data():
	if 'id' not in request.args:
		raise exceptions.InvalidRequestError()
	if 'num' not in request.args:
		raise exceptions.InvalidRequestError()
	if 'interval' not in request.args:
		raise exceptions.InvalidRequestError()
	id = int(request.args['id'])
	num_samples = int(request.args['num'])
	interval = int(request.args['interval'])
	try:
		obj = app.DEVICE.objects[id]
	except KeyError:
		raise exceptions.ObjectDoesNotExistError()
	historic_data = obj.get_historic_data(num_samples, interval)
	return make_response(jsonify({'data': historic_data, 'objname': obj.name}), 200)


@app.route('/auth/set/', methods=['POST'])
@util.crossdomain(origin='*')
def set_pin():
	if 'cpin' not in request.form:
		raise exceptions.InvalidRequestError()
	if 'npin' not in request.form:
		raise exceptions.InvalidRequestError()
	cpin = int(request.form['cpin'])
	npin = int(request.form['npin'])
	if cpin != app.AUTH_PIN:
		return make_response(jsonify({'success': False}), 401)
	app.AUTH_PIN = npin
	return make_response(jsonify({'success': True}), 200)


@app.route('/auth/verify/', methods=['GET'])
@util.crossdomain(origin='*')
def check_pin():
	if 'pin' not in request.args:
		raise exceptions.InvalidRequestError()
	pin = int(request.args['pin'])
	if pin != app.AUTH_PIN:
		return make_response(jsonify({'success': False}), 401)
	return make_response(jsonify({'success': True}), 200)

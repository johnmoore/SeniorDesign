from flask import make_response
from functools import update_wrapper
from hmi.mocks.MockFCDevice import MockFCDevice
from hmi.mocks.MockFCObject import MockFCObject

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

def init_debug_device():
    test_device = MockFCDevice()
    test_device.add_object(MockFCObject(0, 'Rm 113 Temperature', 72.1, 'F'))
    test_device.add_object(MockFCObject(1, 'Rm 113 Humidity', 20.5, '%'))
    test_device.add_object(MockFCObject(2, 'Rm 113 Lighting', 80, '%'))
    test_device.add_object(MockFCObject(3, 'HVAC Fan Speed', 'LO', None))
    test_device.add_object(MockFCObject(4, 'Fire Alarm System', 'OK', None, False))
    return test_device

def Success():
    return make_response("", 200)
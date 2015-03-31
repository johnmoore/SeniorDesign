from flask import make_response
from functools import update_wrapper
from hmi.mocks.MockFCDevice import MockFCDevice
from hmi.mocks.MockFCObject import MockFCObject
from hmi.impl.BacNETFCDevice import BacNETFCDevice
from hmi.impl.BacNETFCObject import BacNETFCObject

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
    test_device.add_object(MockFCObject('analogInput', 0, 'Rm 113 Tesmperature', 72.1, 'F', True))
    test_device.add_object(MockFCObject('analogInput', 1, 'Rm 113 Humidity', 20.5, '%', True))
    test_device.add_object(MockFCObject('analogInput', 2, 'Rm 113 Lighting', 80, '%', True))
    test_device.add_object(MockFCObject('analogInput', 3, 'HVAC Fan Speed', 'LO', None, True))
    return test_device

def Success():
    return make_response("", 200)

def init_hmi_device():
    hmi_device = BacNETFCDevice(10001)
    hmi_device.initialize()
    #hmi_device.add_object(BacNETFCObject(hmi_device, 'analogValue', 201))
    return hmi_device
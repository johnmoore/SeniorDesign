import hmi.tests
import sys


class NoTestSpecifiedError(Exception):
	pass


class InvalidTestSpecifiedError(Exception):
	pass


if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise NoTestSpecifiedError()
	if sys.argv[1] == "all":
		for _, test_class in hmi.tests.test_classes.items():
			test = test_class()
			test.run_test()
	else:
		test = None
		try:
			test = hmi.tests.test_classes[sys.argv[1]]()
		except KeyError:
			raise InvalidTestSpecifiedError()
		test.run_test()

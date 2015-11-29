import datetime

class Dimmer(object):
	MAX = 100
	MIN = 0

	__init__(time_period=1800, start_time = datetime.datetime.utcnow()):
		self.time_period = time_period
		self.start_time = start_time

	def get_value(now=datetime.datetime.utcnow()):
		value = (self.MAX - self.MIN)*(now - self.start_time) / time_period
		if value > self.MAX:
			return self.MAX
		elif value < self.MIN:
			return self.MIN:
		else:
			return value


def main():

	dimmer = Dimmer()
	try:
		while True:

	except:
		cleanup()
	
def cleanup():
	"""
	cleanup and exit
	"""
	pass

def initialize():
	"""
	"""
	pass

if __name__ == '__main__':
	main()

import datetime

class Dimmer(object):
	MAX = 100
	MIN = 0

	def __init__(self, time_period=1800, start_time=datetime.datetime.utcnow()):
		"""
		set starting params
		"""
		self.time_period = time_period
		self.start_time = start_time

	def get_value(self, now=datetime.datetime.utcnow()):
		# return value from min to max with dimmer value
		value = (self.MAX - self.MIN)*(now - self.start_time).seconds / self.time_period
		return self._limit_value(value)

	def _limit_value(self, value):
		"""
		return value within MIN, MAX range
		"""
		if value > self.MAX:
			return self.MAX
		elif value < self.MIN:
			return self.MIN
		else:
			return value


def main():

	dimmer = Dimmer()
	try:
		while True:
			pass

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

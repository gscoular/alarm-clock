import datetime

from lib.neopixel import Adafruit_NeoPixel

import settings

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

class Lights(Adafruit_NeoPixel):
	def __init__(self, n_lights=settings.N_LIGHTS, control_pin=settings.CONTROL_PIN):
		super(Lights, self).__init__(n_lights, control_pin)
		self.begin()
		for light in range(n_lights):
			self.setPixelColorRGB(light, 200, 200, 200)
		self.setBrightness(255)
		self.show()


def main():
	lights = Lights()
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

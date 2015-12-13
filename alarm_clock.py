import datetime

from lib.neopixel import Adafruit_NeoPixel

import settings

class Dimmer(object):
	MAX = 255
	MIN = 0

	def __init__(self, time_period=1800, start_time=datetime.datetime.utcnow()):
		"""
		set starting params
		"""
		self.time_period = time_period
		self.start_time = start_time

	def get_value(self, now=None):
		# return value from min to max with dimmer value
		if now == None:
			now = datetime.datetime.utcnow()
		value = int((self.MAX - self.MIN)*(now - self.start_time).seconds / float(self.time_period))
		
		return self._limit_value(value)

	def _limit_value(self, value):
		"""
		return value within MIN, MAX range
		"""
		if value > self.MAX:
			#reset
			self.start_time = datetime.datetime.utcnow()
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
			self.setPixelColorRGB(light, settings.COLOR[0], settings.COLOR[1], settings.COLOR[2])
		self.setBrightness(0)
		self.show()


def main():
	lights = Lights()
	dimmer = Dimmer(time_period=100)
	try:
		while True:
			print dimmer.get_value()
			lights.setBrightness(dimmer.get_value())
			lights.show()
	except KeyboardInterrupt:
		print "keyboard interrupt: exiting"
		cleanup(lights)	
def cleanup(lights):
	"""
	cleanup and exit
	"""
	lights.setBrightness(0)
	lights.show()
	

if __name__ == '__main__':
	main()

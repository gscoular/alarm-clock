import datetime
import logging

from lib.neopixel import Adafruit_NeoPixel
try:
	from RPi import GPIO
except:
	logging.info("can't import RPi.GPIO")

import settings

logging.basicConfig(filename='output.log',level=logging.DEBUG)
logging.info('booting up: time is %r', datetime.datetime.now())
class Dimmer(object):
	MAX = 255
	MIN = 0

	def __init__(self, time_period=1800, start_time=datetime.datetime.now().time()):
		"""
		set starting params
		"""
		self.time_period = time_period
		self.start_time = start_time

	def is_max_value(self):
		if self.get_value() == self.MAX:
			return True
		return False

	def get_value(self, now=None):
		# return value from min to max with dimmer value
		if now == None:
			now = datetime.datetime.now()
			start_time = datetime.datetime.combine(now.date(), self.start_time)
		value = int((self.MAX - self.MIN)*(now - start_time).seconds / float(self.time_period))
		
		return self._limit_value(value)

	def _limit_value(self, value):
		"""
		return value within MIN, MAX range
		"""
		if value > self.MAX:
			#reset
			self.start_time = datetime.datetime.now().time()
			return self.MAX
		elif value < self.MIN:
			return self.MIN
		else:
			return value

class Lights(Adafruit_NeoPixel):
	MAX_BRIGHTNESS = 255
	MIN_BRIGHTNESS = 0
	def __init__(self, n_lights=settings.N_LIGHTS, control_pin=settings.CONTROL_PIN):
		super(Lights, self).__init__(n_lights, control_pin)
		self.begin()
		for light in range(n_lights):
			self.setPixelColorRGB(light, settings.COLOR[0], settings.COLOR[1], settings.COLOR[2])
		self.setBrightness(0)
		self.show()

	def cleanup(self):
		""" Turn off lights """
		self.setBrightness(0)
		self.show()


def setup_reset():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(settings.RESET_PIN, GPIO.IN)


class ResetPinException(Exception):
	pass

def check_for_reset():
	if GPIO.input(settings.RESET_PIN):
		raise ResetPinException()

def brighten_sequence(lights, dimmer):
	while dimmer.is_max_value() == False:
		lights.setBrightness(dimmer.get_value())
		lights.show()
		check_for_reset()

def bright_lights_sequence(lights, time_period=1800):
	startdate = datetime.datetime.now()
	lights.setBrightness(lights.MAX_BRIGHTNESS)
	lights.show()
	while datetime.datetime.now().time() < (startdate+datetime.timedelta(seconds=time_period)).time():
		check_for_reset()

def main_loop(lights):
	while True:
		current_date = datetime.datetime.now()
		start_date = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(**settings.START_TIME))
		if current_date.time() > start_date.time() and current_date.time() < (start_date+datetime.timedelta(seconds=1800)).time():
			try:
				dimmer = Dimmer(time_period=1800, start_time=datetime.time(**settings.START_TIME))
				print 'brightening lights'
				print dimmer.get_value()
				brighten_sequence(lights, dimmer)
				print 'lights stay on'
				print dimmer.get_value()
				#bright_lights_sequence(lights, time_period=1800)
				print 'sequence over'
			except ResetPinException:
				print "Resetting"
			lights.cleanup()
		else:
			pass
			
def main():
	print 'booting up: %r' %datetime.datetime.now()
	setup_reset()
	lights = Lights()
	try:
		main_loop(lights)
	except KeyboardInterrupt:
		print "keyboard interrupt: exiting"
		lights.cleanup()
	lights.cleanup()
	

if __name__ == '__main__':
	main()

import unittest
import mock
import datetime

from alarm_clock import Dimmer, Lights

class MockNeopixel(object):
	pass
	

class RpiTestCase(unittest.TestCase):
	def setUp(self):
		self.MOCK_NEOPIXEL = mock.patch('lib.neopixel.Adafruit_NeoPixel', return_value = MockNeopixel())
		self.MOCK_NEOPIXEL.start()
		self.MOCK_WS = mock.patch('lib._rpi_ws281x')
		self.MOCK_WS.start()

	def tearDown(self):
		self.MOCK_NEOPIXEL.stop()
		self.MOCK_WS.stop()


class DimmerLimitValuesTests(RpiTestCase):

	def test_limit_values_returns_max_if_value_is_greater_than_max(self):
		dimmer = Dimmer()
		value = dimmer._limit_value(dimmer.MAX+1)
		self.assertEqual(dimmer.MAX, value)

	def test_limit_values_returns_min_if_value_is_less_than_min(self):
		dimmer = Dimmer()
		value = dimmer._limit_value(dimmer.MIN-1)
		self.assertEqual(dimmer.MIN, value)

	def test_returns_value_within_max_min_range(self):
		dimmer = Dimmer()
		value = dimmer._limit_value(dimmer.MIN + 1)
		self.assertEqual(dimmer.MIN+1, value)

class DimmerGetValueTests(RpiTestCase):
	def setUp(self):
		super(DimmerGetValueTests, self).setUp()
		self.start_time = datetime.datetime.utcnow()
		self.dimmer = Dimmer(start_time=self.start_time)

	@mock.patch('alarm_clock.Dimmer._limit_value')
	def test_get_value_calls_limit_value_with_zero_if_start_time(self, mock_limit):
		self.dimmer.get_value(self.start_time)
		mock_limit.assert_called_once_with(0)

	@mock.patch('alarm_clock.Dimmer._limit_value')
	def test_get_value_calls_limit_value_with_max_if_time_period_added_to_start_time(self, mock_limit):
		self.dimmer.get_value(self.start_time+datetime.timedelta(seconds=self.dimmer.time_period))
		mock_limit.assert_called_once_with(self.dimmer.MAX)

	@mock.patch('alarm_clock.Dimmer._limit_value')
	def test_get_value_calls_limit_value_with_half_max_if_half_time_period_added_to_start_time(self, mock_limit):
		self.dimmer.get_value(self.start_time+datetime.timedelta(seconds=self.dimmer.time_period/2))
		mock_limit.assert_called_once_with(self.dimmer.MAX/2)

class LightsTests(RpiTestCase):
	def setUp(self):
		super(LightsTests, self).setUp()

	def test_init_calls_set_pixel_brightness_for_each_light(self):
		light = Lights()
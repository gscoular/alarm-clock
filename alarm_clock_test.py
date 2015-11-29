import unittest
import mock
import datetime

from alarm_clock import Dimmer

class DimmerTests(unittest.TestCase):
	def setUp(self):
		super(DimmerTests, self).setUp()


class DimmerLimitValuesTests(unittest.TestCase):
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

class DimmerGetValueTests(unittest.TestCase):
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

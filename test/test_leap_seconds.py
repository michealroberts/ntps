# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from ntps.leap_seconds import LEAP_SECONDS, get_leap_indicator

# **************************************************************************************


class TestLeapIndicator(unittest.TestCase):
    def test_within_warning_window(self):
        """
        Test that if the timestamp is less than 60 seconds before a leap event,
        the function returns 1.
        """
        # Use the first leap event from the list for testing.
        leap_event = LEAP_SECONDS[0]
        # Simulate a timestamp 59 seconds before the leap event.
        test_timestamp = leap_event - 59
        self.assertEqual(
            get_leap_indicator(test_timestamp),
            1,
            f"Expected LI=1 for timestamp {test_timestamp}, 59 seconds before the leap event {leap_event}",
        )

    def test_exactly_at_warning_threshold(self):
        """
        Test that if the timestamp is exactly 60 seconds before the leap event,
        the function returns 0 (warning window is strictly less than 60).
        """
        leap_event = LEAP_SECONDS[0]
        test_timestamp = leap_event - 60
        self.assertEqual(
            get_leap_indicator(test_timestamp),
            0,
            f"Expected LI=0 for timestamp {test_timestamp}, exactly 60 seconds before the leap event {leap_event}",
        )

    def test_outside_warning_window(self):
        """
        Test that if the timestamp is more than 60 seconds before a leap event,
        the function returns 0.
        """
        leap_event = LEAP_SECONDS[0]
        # Simulate a timestamp 61 seconds before the leap event.
        test_timestamp = leap_event - 61
        self.assertEqual(
            get_leap_indicator(test_timestamp),
            0,
            f"Expected LI=0 for timestamp {test_timestamp}, 61 seconds before the leap event {leap_event}",
        )

    def test_no_upcoming_leap(self):
        """
        Test that if there is no upcoming leap event (timestamp is after the last event),
        the function returns 0.
        """
        # Use a timestamp that is well after the last leap event.
        test_timestamp = LEAP_SECONDS[-1] + 1000
        self.assertEqual(
            get_leap_indicator(test_timestamp),
            0,
            f"Expected LI=0 for timestamp {test_timestamp}, after the last leap event",
        )


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

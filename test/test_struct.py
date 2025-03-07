# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from struct import pack

from ntps import pack_timestamp

# **************************************************************************************


class TestPackTimestamp(unittest.TestCase):
    def test_zero(self) -> None:
        """
        Test that packing a timestamp of 0.0 produces an 8-byte string of all zeros:
        """
        result = pack_timestamp(0.0)
        expected = pack("!I", 0) + pack("!I", 0)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 8)

    def test_known_value(self) -> None:
        """
        Test that packing a known timestamp (e.g., 1.5) produces the expected result.
        The integer part of 1.5 is 1 and the fractional part is 0.5 * 2**32.
        """
        timestamp = 1.5
        result = pack_timestamp(timestamp)
        integer = 1
        fraction = int((timestamp - integer) * (2**32))
        expected = pack("!I", integer) + pack("!I", fraction)
        self.assertEqual(result, expected)

    def test_length(self) -> None:
        """
        Test that the packed timestamp always returns an 8-byte string.
        """
        timestamp = 12345.6789
        result = pack_timestamp(timestamp)
        self.assertEqual(len(result), 8)

    def test_fraction_precision(self) -> None:
        """
        Test that the fractional part is computed correctly for a non-integer timestamp.
        """
        timestamp = 3.141592653589793
        result = pack_timestamp(timestamp)
        integer = int(timestamp)
        fraction = int((timestamp - integer) * (2**32))
        expected = pack("!I", integer) + pack("!I", fraction)
        self.assertEqual(result, expected)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

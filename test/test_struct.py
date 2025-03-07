# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from struct import pack

from ntps import pack_timestamp, unpack_timestamp

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


class TestUnpackTimestamp(unittest.TestCase):
    def test_unpack_zero(self) -> None:
        """
        Test that unpacking an 8-byte timestamp of all zeros returns 0.0:
        """
        # Pack zero seconds and zero fractional seconds:
        data = pack("!I I", 0, 0)
        result = unpack_timestamp(data)
        self.assertEqual(result, 0.0)

    def test_unpack_known_value(self) -> None:
        """
        Test that unpacking a known 8-byte timestamp returns the expected float value:
        """
        # Define a known timestamp value, e.g., 1.5 (integer part 1 and fractional part 0.5):
        integer = 1
        fraction = int(0.5 * (2**32))
        data = pack("!I I", integer, fraction)
        result = unpack_timestamp(data)
        self.assertAlmostEqual(result, 1.5, places=7)

    def test_invalid_length(self) -> None:
        """
        Test that unpacking data with invalid length raises a ValueError:
        """
        # Create data with an invalid length (7 bytes instead of 8):
        data = b"\x00" * 7
        with self.assertRaises(ValueError):
            unpack_timestamp(data)

    def test_round_trip(self) -> None:
        """
        Test that packing a timestamp and then unpacking it yields the original timestamp:
        """
        # Define an arbitrary timestamp value:
        timestamp = 12345.6789
        # Pack the timestamp into an 8-byte format:
        data = pack_timestamp(timestamp)
        # Unpack the data back into a float:
        result = unpack_timestamp(data)
        # Check that the original timestamp and the round-trip result are almost equal:
        self.assertAlmostEqual(result, timestamp, places=6)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

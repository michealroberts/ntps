# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from struct import unpack

from ntps import NTPPacket, NTPPacketParameters

# **************************************************************************************


class TestNTPPacketParameters(unittest.TestCase):
    def test_valid_parameters(self) -> None:
        """
        Test that a valid NTPPacketParameters dictionary contains the expected keys
        and that the values are of the correct type.
        """
        params: NTPPacketParameters = {
            "LI": 0,
            "version": 4,
            "mode": 4,
            "stratum": 0,
            "poll": 0,
            "precision": -20,
            "root_delay": 0.0,
            "root_dispersion": 0.0,
            "reference_id": 12345,
            "reference_timestamp": 1620000000.0,
            "originate_timestamp_low": 1620000001,
            "originate_timestamp_high": 1620000001,
            "rx_timestamp": 1620000002.0,
            "tx_timestamp": 1620000003.0,
        }

        expected_keys = {
            "LI",
            "version",
            "mode",
            "stratum",
            "poll",
            "precision",
            "root_delay",
            "root_dispersion",
            "reference_id",
            "reference_timestamp",
            "originate_timestamp_low",
            "originate_timestamp_high",
            "rx_timestamp",
            "tx_timestamp",
        }
        self.assertEqual(set(params.keys()), expected_keys)
        self.assertIsInstance(params["LI"], int)
        self.assertIsInstance(params["version"], int)
        self.assertIsInstance(params["mode"], int)
        self.assertIsInstance(params["stratum"], int)
        self.assertIsInstance(params["poll"], int)
        self.assertIsInstance(params["precision"], int)
        self.assertIsInstance(params["root_delay"], float)
        self.assertIsInstance(params["root_dispersion"], float)
        self.assertIsInstance(params["reference_id"], int)
        self.assertIsInstance(params["reference_timestamp"], float)
        self.assertIsInstance(params["originate_timestamp_low"], int)
        self.assertIsInstance(params["originate_timestamp_high"], int)
        self.assertIsInstance(params["rx_timestamp"], float)
        self.assertIsInstance(params["tx_timestamp"], float)

    def test_missing_key(self) -> None:
        """
        Test that a dictionary missing a required key does not match the expected keys.
        (Note: at runtime, TypedDict is just a dict, so this test checks key presence.)
        """
        params = {
            "LI": 0,
            "version": 4,
            "mode": 4,
            "stratum": 0,
            "poll": 0,
            "precision": -20,
            "root_delay": 0.0,
            "root_dispersion": 0.0,
            # "reference_id" is omitted intentionally:
            "reference_timestamp": 1620000000.0,
            "originate_timestamp": 1620000001.0,
            "rx_timestamp": 1620000002.0,
            "tx_timestamp": 1620000003.0,
        }
        expected_keys = {
            "LI",
            "version",
            "mode",
            "stratum",
            "poll",
            "precision",
            "root_delay",
            "root_dispersion",
            "reference_id",
            "reference_timestamp",
            "originate_timestamp",
            "rx_timestamp",
            "tx_timestamp",
        }
        self.assertNotEqual(set(params.keys()), expected_keys)
        self.assertNotIn("reference_id", params.keys())


# **************************************************************************************


class TestNTPPacket(unittest.TestCase):
    def setUp(self) -> None:
        # Create a sample NTPPacketParameters dictionary with known values:
        # The reference_id is derived from the bytes for "GPS\x00".
        reference_id = unpack("!I", b"GPS\x00")[0]
        self.params: NTPPacketParameters = {
            "LI": 0,  # Leap Indicator: 0 (no warning)
            "version": 4,  # NTP version: 4
            "mode": 4,  # Mode: 4 (server)
            "stratum": 0,  # Stratum: 0 (primary reference)
            "poll": 0,  # Poll interval: example value 0
            "precision": -20,  # Precision: example value in log₂ seconds
            "root_delay": 0.0,  # Root delay: 0.0 seconds
            "root_dispersion": 0.0,  # Root dispersion: 0.0 seconds
            "reference_id": reference_id,  # Reference ID: from "GPS\x00"
            "reference_timestamp": 1000.0,  # Reference timestamp: example value
            "originate_timestamp_low": 1001,  # Originate timestamp low: example value
            "originate_timestamp_high": 1001,  # Originate timestamp high: example value
            "rx_timestamp": 1002.0,  # Receive timestamp: example value
            "tx_timestamp": 1003.0,  # Transmit timestamp: example value
        }

    def test_to_bytes_length(self) -> None:
        """
        Verify that to_bytes() returns exactly 48 bytes.
        """
        packet = NTPPacket(self.params)
        data = packet.to_bytes()
        self.assertEqual(len(data), 48)

    def test_round_trip(self) -> None:
        """
        Verify that converting a packet to bytes and then back using from_bytes()
        results in an NTPPacket with equivalent parameters.
        """
        packet = NTPPacket(self.params)
        data = packet.to_bytes()
        new_packet = NTPPacket.from_bytes(data)

        # Check integer fields for equality:
        self.assertEqual(new_packet.LI, self.params["LI"])
        self.assertEqual(new_packet.version, self.params["version"])
        self.assertEqual(new_packet.mode, self.params["mode"])
        self.assertEqual(new_packet.stratum, self.params["stratum"])
        self.assertEqual(new_packet.poll, self.params["poll"])
        self.assertEqual(new_packet.precision, self.params["precision"])
        self.assertEqual(new_packet.reference_id, self.params["reference_id"])

        # Check float fields using assertAlmostEqual due to potential minor floating point differences:
        self.assertAlmostEqual(
            new_packet.root_delay, self.params["root_delay"], places=6
        )
        self.assertAlmostEqual(
            new_packet.root_dispersion, self.params["root_dispersion"], places=6
        )
        self.assertAlmostEqual(
            new_packet.reference_timestamp, self.params["reference_timestamp"], places=6
        )
        self.assertAlmostEqual(
            new_packet.originate_timestamp_low,
            self.params["originate_timestamp_low"],
            places=6,
        )
        self.assertAlmostEqual(
            new_packet.originate_timestamp_high,
            self.params["originate_timestamp_high"],
            places=6,
        )
        self.assertAlmostEqual(
            new_packet.rx_timestamp, self.params["rx_timestamp"], places=6
        )
        self.assertAlmostEqual(
            new_packet.tx_timestamp, self.params["tx_timestamp"], places=6
        )

    def test_from_bytes_invalid_length(self) -> None:
        """
        Verify that from_bytes() raises a ValueError if the data length is less than 48 bytes.
        """
        with self.assertRaises(ValueError):
            NTPPacket.from_bytes(b"\x00" * 47)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

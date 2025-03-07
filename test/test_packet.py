# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest

from ntps.packet import NTPPacketParameters  # Import the TypedDict definition

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
        self.assertIsInstance(params["originate_timestamp"], float)
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

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

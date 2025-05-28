# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from time import time

from ntps.correction import NTPCorrection, get_ntp_offset_correction
from ntps.packet import NTPPacket, NTPPacketParameters
from ntps.system import NTP_TIMESTAMP_DELTA

# **************************************************************************************


class TestNTPCorrection(unittest.TestCase):
    def setUp(self) -> None:
        self.t1 = 10000.5
        self.t2 = 10010.5
        self.t3 = 10020.5
        self.t4 = 10000.5
        self.expected_delay = (self.t4 - self.t1) - (self.t3 - self.t2)
        self.expected_offset = ((self.t2 - self.t1) + (self.t3 - self.t4)) / 2
        self.expected_unix = (self.t3 - NTP_TIMESTAMP_DELTA) + self.expected_offset

    def make_packet(
        self, now: float, latency_in: float = 0.0, latency_out: float = 0.0
    ) -> NTPPacket:
        t1 = now - latency_in
        t2 = now
        t3 = now + latency_out

        originate_timestamp_high = int(t1)
        originate_timestamp_low = int((t1 - originate_timestamp_high) * 2**32)

        params = NTPPacketParameters(
            LI=0,
            version=4,
            mode=3,
            stratum=1,
            poll=6,
            precision=0,
            root_delay=0.0,
            root_dispersion=0.0,
            reference_id=0,
            reference_timestamp=0.0,
            originate_timestamp_high=originate_timestamp_high,
            originate_timestamp_low=originate_timestamp_low,
            rx_timestamp=t2,
            tx_timestamp=t3,
        )

        return NTPPacket(params)

    def test_zero_latency(self) -> None:
        now = time()
        ntp = time() + NTP_TIMESTAMP_DELTA
        packet = self.make_packet(ntp, latency_in=0.0, latency_out=0.0)
        correction: NTPCorrection = get_ntp_offset_correction(packet)

        self.assertAlmostEqual(correction["delay"], 0.0, places=4)
        self.assertAlmostEqual(correction["offset"], 0.0, places=4)
        self.assertTrue(abs(correction["unix"] - now) < 0.00001)
        self.assertTrue(correction["start"] >= ntp)

    def test_small_symmetric_latency(self) -> None:
        now = time()
        ntp = now + NTP_TIMESTAMP_DELTA
        latency = 0.1
        packet = self.make_packet(ntp, latency_in=latency, latency_out=latency)
        correction: NTPCorrection = get_ntp_offset_correction(packet)

        self.assertAlmostEqual(correction["delay"], 0.0, places=4)
        self.assertAlmostEqual(correction["offset"], latency, places=4)
        self.assertTrue(abs(correction["unix"] - (now + latency)) < 0.1)
        self.assertTrue(correction["start"] >= ntp)

    def test_asymmetric_latency(self) -> None:
        now = time()
        ntp = now + NTP_TIMESTAMP_DELTA
        latency_in = 0.2
        latency_out = 0.5
        packet = self.make_packet(ntp, latency_in=latency_in, latency_out=latency_out)
        correction: NTPCorrection = get_ntp_offset_correction(packet)

        expected_delay = (ntp - (ntp - latency_in)) - ((ntp + latency_out) - ntp)
        expected_offset = (
            ((ntp) - (ntp - latency_in)) + ((ntp + latency_out) - ntp)
        ) / 2
        expected_unix = ((ntp + latency_out) - NTP_TIMESTAMP_DELTA) + expected_offset

        self.assertAlmostEqual(correction["delay"], expected_delay, places=3)
        self.assertAlmostEqual(correction["offset"], expected_offset, places=3)
        self.assertAlmostEqual(correction["unix"], expected_unix, places=3)

    def test_fractional_precision(self) -> None:
        now = time()
        ntp = now + NTP_TIMESTAMP_DELTA
        fractional = 0.12345678
        packet = self.make_packet(ntp + fractional, latency_in=0.0, latency_out=0.0)
        reconstructed_t1 = (
            packet.originate_timestamp_high + packet.originate_timestamp_low / 2**32
        )
        self.assertAlmostEqual(reconstructed_t1, ntp + fractional, places=6)
        correction: NTPCorrection = get_ntp_offset_correction(packet)
        self.assertAlmostEqual(abs(correction["offset"]), fractional / 2, places=4)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

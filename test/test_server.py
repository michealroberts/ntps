# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from asyncio import DatagramTransport
from unittest.mock import MagicMock, patch

from ntps.server import NTPServer

# **************************************************************************************


# Define a custom NTP test server that uses GPS-synced time as the reference time, and a
# stratum level of 0:
class GNSSStratum0NTPServer(NTPServer):
    # Set the reference identifier of the NTP server:
    refid = "GPS"
    # Set the stratum level of the NTP server:
    stratum = 0


# **************************************************************************************


class TestNTPServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = GNSSStratum0NTPServer()

    def test_initialization_default_stratum(self) -> None:
        default_server = NTPServer()
        self.assertEqual(default_server.stratum, 0)

    @patch("ntps.server.get_ntp_time", return_value=1234567890.123456)
    def test_get_ntp_time(self, mock_get_ntp_time):
        self.assertEqual(self.server.get_ntp_time(), 1234567890.123456)

    def test_connection_made(self):
        transport = MagicMock(spec=DatagramTransport)
        self.server.connection_made(transport)
        self.assertEqual(self.server.transport, transport)

    @patch("ntps.server.get_ntp_time", return_value=1234567890.123456)
    @patch("ntps.server.time_ns", side_effect=[1000000000, 1001000000])
    @patch("ntps.server.get_leap_indicator", return_value=0)
    @patch("ntps.server.NTPPacket")
    def test_datagram_received_valid_packet(
        self, mock_packet_cls, mock_leap_indicator, mock_time_ns, mock_get_ntp_time
    ) -> None:
        transport = MagicMock(spec=DatagramTransport)
        self.server.connection_made(transport)

        data = bytearray(48)
        data[40:48] = b"\x00\x00\x00\x00\x00\x00\x00\x01"

        mock_packet = MagicMock()
        mock_packet.to_bytes.return_value = b"response"
        mock_packet_cls.return_value = mock_packet

        addr = ("127.0.0.1", 123)

        self.server.datagram_received(bytes(data), addr)

        mock_packet_cls.assert_called()
        transport.sendto.assert_called_once_with(b"response", addr)

    @patch("ntps.server.get_ntp_time", return_value=1234567890.123456)
    @patch("ntps.server.time_ns", side_effect=[1000000000, 1001000000])
    @patch("ntps.server.get_leap_indicator", return_value=0)
    @patch("ntps.server.NTPPacket")
    def test_datagram_received_short_packet(
        self, mock_packet_cls, mock_leap_indicator, mock_time_ns, mock_get_ntp_time
    ) -> None:
        transport = MagicMock(spec=DatagramTransport)
        self.server.connection_made(transport)

        data = b""

        mock_packet = MagicMock()
        mock_packet.to_bytes.return_value = b"response"
        mock_packet_cls.return_value = mock_packet

        addr = ("127.0.0.1", 123)

        self.server.datagram_received(data, addr)

        mock_packet_cls.assert_called()
        transport.sendto.assert_called_once_with(b"response", addr)

    def test_datagram_received_no_transport(self) -> None:
        self.server.transport = None

        data = b"\x00" * 48
        addr = ("127.0.0.1", 123)

        with patch.object(self.server, "get_ntp_time") as mock_ntp_time:
            self.server.datagram_received(data, addr)

        mock_ntp_time.assert_not_called()


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************

# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import struct
from asyncio import DatagramProtocol, DatagramTransport
from time import time_ns
from typing import Final, Literal, Optional, Tuple, cast

from .leap_seconds import get_leap_indicator
from .packet import NTPPacket, NTPPacketParameters
from .refid import ReferenceID
from .system import get_ntp_time

# **************************************************************************************


class NTPServer(DatagramProtocol):
    refid: ReferenceID | Literal["UNKN"] = "UNKN"

    stratum: Literal[0, 1, 2, 3, 4] = 0

    transport: Optional[DatagramTransport] = None

    address: Final[Tuple[str, int]] = ("0.0.0.0", 123)

    def __init__(self) -> None:
        super().__init__()

    def get_ntp_time(self) -> float:
        return get_ntp_time()

    def connection_made(self, transport: DatagramTransport) -> None:  # type: ignore[override]
        self.transport = cast(DatagramTransport, transport)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        # Check if the server reference identifier is set to a valid value:
        if self.refid == "UNKN" or self.refid == "":
            raise ValueError(
                "The server reference identifier must be set to a valid value."
            )

        # Check if the transport is available; if not, exit early:
        if self.transport is None:
            return

        # Capture the raw originate timestamp bytes (or zeros if missing):
        originate_bytes = data[40:48] if len(data) >= 48 else b"\x00" * 8

        originate_timestamp_high, originate_timestamp_low = struct.unpack(
            "!II", originate_bytes
        )

        rx_timestamp: float = self.get_ntp_time()

        # Obtain the time (in nanoseconds) before we get_ntp_time():
        before = time_ns()

        # Retrieve the current system time as the reference timestamp:
        reference_timestamp: float = self.get_ntp_time()

        # Obtain the time (in nanoseconds) after we get_ntp_time():
        after = time_ns()

        # Get the delay in the number of seconds when obtaining the synced system time:
        delay = (after - before) * 1e-9

        # Get the leap indicator from the current reference timestamp:
        li: int = get_leap_indicator(timestamp=reference_timestamp)

        # Convert the reference identifier into a bytes buffer for unpacking, ensuring that the
        # encoding value is exactly 4 bytes long:
        refid_buffer: bytes = self.refid.encode("ascii").ljust(4, b"\x00")[:4]

        # Convert the reference identifier into a bytes buffer for unpacking, ensuring that the
        # encoding value is exactly 4 bytes long:
        reference_id: int = struct.unpack("!I", refid_buffer)[0]

        # Retrieve the current system time to be used as the transmit timestamp:
        tx_timestamp: float = self.get_ntp_time()

        # Build the parameters dictionary for the NTP response packet:
        params: NTPPacketParameters = {
            "LI": li,
            "version": 4,
            "mode": 4,
            "stratum": self.stratum,
            "poll": 6,
            "precision": -20,
            "root_delay": delay,
            "root_dispersion": 0.001,
            "reference_id": reference_id,
            "reference_timestamp": reference_timestamp,  # T0
            "originate_timestamp_high": originate_timestamp_high,  # T1
            "originate_timestamp_low": originate_timestamp_low,  # T1
            "rx_timestamp": rx_timestamp,  # T2
            "tx_timestamp": tx_timestamp,  # T3
        }

        # Create an NTPPacket instance using the defined parameters:
        packet = NTPPacket(params=params)
        # Convert the NTPPacket into a 48-byte binary packet:
        packet_bytes: bytes = packet.to_bytes()
        # Send the binary packet to the client at the specified address:
        self.transport.sendto(packet_bytes, addr)
        # Log that the NTP response was sent:
        print(f"Sent NTP response to {addr} using system time (GPS-synced).")


# **************************************************************************************

# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from struct import pack, unpack
from typing import TypedDict

from .struct import pack_timestamp, unpack_timestamp

# **************************************************************************************


class NTPPacketParameters(TypedDict):
    LI: int
    version: int
    mode: int
    stratum: int
    poll: int
    precision: int
    root_delay: float
    root_dispersion: float
    reference_id: int
    reference_timestamp: float
    originate_timestamp_low: int
    originate_timestamp_high: int
    rx_timestamp: float
    tx_timestamp: float


# **************************************************************************************


class NTPPacket(object):
    def __init__(self, params: NTPPacketParameters) -> None:
        self.LI: int = params["LI"]
        self.version: int = params["version"]
        self.mode: int = params["mode"]
        self.stratum: int = params["stratum"]
        self.poll: int = params["poll"]
        self.precision: int = params["precision"]
        self.root_delay: float = params["root_delay"]
        self.root_dispersion: float = params["root_dispersion"]
        self.reference_id: int = params["reference_id"]
        self.reference_timestamp: float = params["reference_timestamp"]
        self.originate_timestamp_high = params["originate_timestamp_high"]
        self.originate_timestamp_low = params["originate_timestamp_low"]
        self.rx_timestamp: float = params["rx_timestamp"]
        self.tx_timestamp: float = params["tx_timestamp"]

    def to_bytes(self) -> bytes:
        # Build the first byte by combining LI (2 bits), version (3 bits), and mode (3 bits):
        LI_VN_Mode: int = (self.LI << 6) | (self.version << 3) | self.mode
        # Pack the header fields (LI_VN_Mode, stratum, poll, precision) into a byte string:
        packet = pack("!B B B b", LI_VN_Mode, self.stratum, self.poll, self.precision)
        # Pack the root delay as a 16.16 fixed-point value:
        packet += pack("!I", int(self.root_delay * (2**16)))
        # Pack the root dispersion as a 16.16 fixed-point value:
        packet += pack("!I", int(self.root_dispersion * (2**16)))
        # Pack the reference ID as a 32-bit integer:
        packet += pack("!I", self.reference_id)
        # Pack the reference timestamp into an 8-byte NTP timestamp:
        packet += pack_timestamp(self.reference_timestamp)
        # Pack the originate timestamp into an 8-byte NTP timestamp:
        packet += pack(
            "!I I", self.originate_timestamp_high, self.originate_timestamp_low
        )
        # Pack the receive timestamp into an 8-byte NTP timestamp:
        packet += pack_timestamp(self.rx_timestamp)
        # Pack the transmit timestamp into an 8-byte NTP timestamp:
        packet += pack_timestamp(self.tx_timestamp)
        # Return the complete 48-byte packet:
        return packet

    @classmethod
    def from_bytes(cls, data: bytes) -> "NTPPacket":
        """
        Unpack a 48-byte data packet into an NTPPacket
        """
        # Check that the provided data has at least 48 bytes:
        if len(data) < 48:
            raise ValueError("Data is too short to be a valid NTP packet")

        # Unpack the first 4 bytes to retrieve the header (LI_VN_Mode, stratum, poll, precision):
        first_byte, stratum, poll, precision = unpack("!B B B b", data[:4])

        # Extract the Leap Indicator from the first 2 bits of the header:
        LI: int = (first_byte >> 6) & 0x3
        # Extract the NTP version from the next 3 bits of the header:
        version: int = (first_byte >> 3) & 0x7
        # Extract the mode from the last 3 bits of the header:
        mode: int = first_byte & 0x7
        # Unpack root delay, root dispersion, and reference ID from bytes 4 to 16:
        root_delay, root_dispersion, reference_id = unpack("!I I I", data[4:16])
        # Convert the root delay from 16.16 fixed-point to a float:
        root_delay = root_delay / (2**16)
        # Convert the root dispersion from 16.16 fixed-point to a float:
        root_dispersion = root_dispersion / (2**16)
        # Unpack the reference timestamp from bytes 16 to 24:
        reference_timestamp = unpack_timestamp(data[16:24])
        # Unpack the originate timestamp from bytes 24 to 32:
        # Capture the raw originate timestamp bytes (or zeros if missing):
        originate_bytes = data[24:32] if len(data) >= 32 else b"\x00" * 8
        originate_timestamp_high, originate_timestamp_low = unpack(
            "!II", originate_bytes
        )
        # Unpack the receive timestamp from bytes 32 to 40:
        rx_timestamp = unpack_timestamp(data[32:40])
        # Unpack the transmit timestamp from bytes 40 to 48:
        tx_timestamp = unpack_timestamp(data[40:48])

        # Construct the parameters dictionary using the specified keys:
        params: NTPPacketParameters = NTPPacketParameters(
            {
                "LI": LI,
                "version": version,
                "mode": mode,
                "stratum": stratum,
                "poll": poll,
                "precision": precision,
                "root_delay": root_delay,
                "root_dispersion": root_dispersion,
                "reference_id": reference_id,
                "reference_timestamp": reference_timestamp,
                "originate_timestamp_high": originate_timestamp_high,
                "originate_timestamp_low": originate_timestamp_low,
                "rx_timestamp": rx_timestamp,
                "tx_timestamp": tx_timestamp,
            }
        )

        # Return a new NTPPacket instance constructed from the parameters:
        return cls(params)


# **************************************************************************************

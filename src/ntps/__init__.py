# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from .client import NTPClient
from .packet import NTPPacket, NTPPacketParameters
from .server import NTPServer
from .struct import pack_timestamp, unpack_timestamp
from .system import NTP_TIMESTAMP_DELTA, get_ntp_time

# **************************************************************************************

__version__ = "0.2.0"

# **************************************************************************************

__license__ = "MIT"

# **************************************************************************************

__all__: list[str] = [
    "__version__",
    "__license__",
    "get_ntp_time",
    "pack_timestamp",
    "unpack_timestamp",
    "NTP_TIMESTAMP_DELTA",
    "NTPClient",
    "NTPPacket",
    "NTPPacketParameters",
    "NTPServer",
]

# **************************************************************************************

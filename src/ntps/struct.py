# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from struct import pack

# **************************************************************************************


def pack_timestamp(timestamp: float) -> bytes:
    """
    Pack a floating-point timestamp into a 64-bit NTP timestamp.

    The first 32 bits are the integer part, the next 32 bits are the fractional part.
    """
    seconds: int = int(timestamp)

    fractional_seconds: int = int((timestamp - seconds) * (2**32))

    return pack("!I", seconds) + pack("!I", fractional_seconds)


# **************************************************************************************

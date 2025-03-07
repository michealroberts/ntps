# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from struct import pack, unpack

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


def unpack_timestamp(data: bytes) -> float:
    """
    Unpack an 8-byte NTP timestamp into a float.
    """
    if len(data) != 8:
        raise ValueError("Invalid timestamp length")

    seconds, fractional_seconds = unpack("!I I", data)

    return seconds + fractional_seconds / (2**32)


# **************************************************************************************

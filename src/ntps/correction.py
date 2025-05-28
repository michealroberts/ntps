# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from time import time
from typing import Callable, TypedDict

from .packet import NTPPacket
from .system import NTP_TIMESTAMP_DELTA

# **************************************************************************************


class NTPCorrection(TypedDict):
    start: float
    delay: float
    offset: float
    unix: float


# **************************************************************************************


def get_ntp_offset_correction(
    packet: NTPPacket, when: Callable[[], float] = lambda: time() + NTP_TIMESTAMP_DELTA
) -> NTPCorrection:
    """
    Calculate the NTP correction values from the given NTP packet.

    This function computes the round-trip delay, offset, and Unix time based on the
    timestamps in the NTP packet. It assumes the packet has valid timestamps.

    Args:
        packet (NTPPacket): The NTP packet containing the timestamps.

    Returns:
        NTPCorrection: A dictionary containing the start time, delay, offset, and Unix time.

    Notes:
        - The `start` time is captured at the beginning of the computation to measure
          the function overhead. This should be used to apply one final correction
          to the final Unix time when setting the system time.
    """
    # Capture start of computation to measure function overhead for further offset
    # correction when setting the system time:
    start = time() + NTP_TIMESTAMP_DELTA

    # T1: Originate timestamp (high + low fractional):
    t1 = packet.originate_timestamp_high + packet.originate_timestamp_low / 2**32

    # T2: Receive timestamp at server:
    t2 = packet.rx_timestamp

    # T3: Transmit timestamp from server:
    t3 = packet.tx_timestamp

    # T4: Destination timestamp (client receive), measured now:
    t4 = when()

    # Calculate the round-trip delay:
    delay = (t4 - t1) - (t3 - t2)

    # Calculate the offset as the average of the two time differences:
    offset = ((t2 - t1) + (t3 - t4)) / 2

    # Compute the Unix time from T3 and the NTP epoch delta:
    unix = (t3 - NTP_TIMESTAMP_DELTA) + offset

    return NTPCorrection(
        start=start,
        delay=delay,
        offset=offset,
        unix=unix,
    )


# **************************************************************************************

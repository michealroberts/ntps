# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import errno
from time import CLOCK_REALTIME, clock_settime, time

# **************************************************************************************

# The delta between the NTP epoch (1900) and the Unix epoch (1970)
NTP_TIMESTAMP_DELTA: int = 2_208_988_800

# **************************************************************************************


def get_ntp_time() -> float:
    """
    Returns the current system time as an NTP timestamp.
    Assumes the system time is GPS-synced externally.
    """
    return time() + NTP_TIMESTAMP_DELTA


# **************************************************************************************


def set_system_time(when: float) -> None:
    """
    Set the system clock (CLOCK_REALTIME) to timestamp (seconds since epoch,
    as a float.

    Raises PermissionError if you're not privileged, or OSError on other failure.
    """
    try:
        clock_settime(CLOCK_REALTIME, when)
    except OSError as e:
        # Map EPERM → PermissionError for clarity:
        if e.errno == errno.EPERM:
            raise PermissionError(
                "setting system time requires root/administrator"
            ) from e
        raise


# **************************************************************************************

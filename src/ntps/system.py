# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from time import time

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

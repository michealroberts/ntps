# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import TypedDict

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
    originate_timestamp: float
    rx_timestamp: float
    tx_timestamp: float


# **************************************************************************************

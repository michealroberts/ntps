# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Literal

# **************************************************************************************

# Define a literal type for the possible reference IDs:
ReferenceID = Literal[
    "GOES",
    "GPS",
    "GAL",
    "PPS",
    "IRIG",
    "WWVB",
    "DCF",
    "HBG",
    "MSF",
    "JJY",
    "LORC",
    "TDF",
    "CHU",
    "WWV",
    "WWVH",
    "NIST",
    "ACTS",
    "USNO",
    "PTB",
    "DFM",
]

# **************************************************************************************

# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from typing import Dict, Final, Literal

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

# Define a dictionary mapping each reference ID to its descriptive comment:
REFERENCE_IDS: Final[Dict[ReferenceID, str]] = {
    "GOES": "Geosynchronous Orbit Environment Satellite",
    "GPS": "Global Positioning System",
    "GAL": "Galileo Positioning System",
    "PPS": "Generic pulse-per-second",
    "IRIG": "Inter-Range Instrumentation Group",
    "WWVB": "LF Radio WWVB Ft. Collins, CO 60 kHz",
    "DCF": "LF Radio DCF77 Mainflingen, DE 77.5 kHz",
    "HBG": "LF Radio HBG Prangins, HB 75 kHz",
    "MSF": "LF Radio MSF Anthorn, UK 60 kHz",
    "JJY": "LF Radio JJY Fukushima, JP 40 kHz, Saga, JP 60 kHz",
    "LORC": "MF Radio LORAN C station, 100 kHz",
    "TDF": "MF Radio Allouis, FR 162 kHz",
    "CHU": "HF Radio CHU Ottawa, Ontario",
    "WWV": "HF Radio WWV Ft. Collins, CO",
    "WWVH": "HF Radio WWVH Kauai, HI",
    "NIST": "NIST telephone modem",
    "ACTS": "NIST telephone modem",
    "USNO": "USNO telephone modem",
    "PTB": "European telephone modem",
    "DFM": "UTC(DFM)",
}

# **************************************************************************************

# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import sys
from datetime import datetime, timezone
from struct import pack

from ntps import NTP_TIMESTAMP_DELTA, NTPClient

# **************************************************************************************

if __name__ == "__main__":
    # Create an instance of NTPClient with the desired endpoint and port:
    client = NTPClient("0.0.0.0")

    # Query the NTP endpoint and print the results:
    try:
        packet = client.query()
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

    # Calculate the server's Unix time by subtracting the NTP epoch delta:
    server_time: float = packet.tx_timestamp - NTP_TIMESTAMP_DELTA

    # Convert the reference ID to a human-readable string:
    reference_id_bytes: bytes = pack("!I", packet.reference_id)

    # Print the server time as a UTC datetime:
    print("Server Time:", datetime.fromtimestamp(server_time, tz=timezone.utc))
    # Print the detailed fields of the received NTP packet:
    print("\nPacket Details:")
    print("  LI:", packet.LI)
    print("  Version:", packet.version)
    print("  Mode:", packet.mode)
    print("  Stratum:", packet.stratum)
    print("  Poll:", packet.poll)
    print("  Precision:", packet.precision)
    print("  Root Delay:", packet.root_delay)
    print("  Root Dispersion:", packet.root_dispersion)
    print("  Reference ID:", reference_id_bytes.decode("ascii").rstrip("\x00"))
    print("  Reference Timestamp:", packet.reference_timestamp)
    print("  Originate Timestamp:", packet.originate_timestamp)
    print("  Receive Timestamp:", packet.rx_timestamp)
    print("  Transmit Timestamp:", packet.tx_timestamp)

# **************************************************************************************

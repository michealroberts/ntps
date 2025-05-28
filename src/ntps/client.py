# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from socket import AF_INET, SOCK_DGRAM, socket
from struct import error as struct_error
from struct import pack_into
from time import time

from .packet import NTPPacket
from .system import NTP_TIMESTAMP_DELTA

# **************************************************************************************


class NTPClient:
    # Default NTP server endpoint (e.g., "pool.ntp.org" or "0.0.0.0"):
    endpoint: str

    # Default port number for NTP communication:
    port: int = 123

    # Default timeout value for the NTP query (in seconds):
    timeout: float = 5.0

    def __init__(self, endpoint: str, port: int = 123, timeout: float = 5.0):
        self.endpoint = endpoint
        self.port = port
        self.timeout = timeout

    def query(self) -> "NTPPacket":
        """
        Query an NTP server for time synchronization data.

        This method sends an NTP request to the configured server endpoint and returns the parsed response.

        Returns:
            NTPPacket: A parsed NTP packet containing time synchronization data.

        Raises:
            TimeoutError: If the NTP request times out according to the configured timeout.
            ConnectionError: If there's an address-related error or socket error during the query.
            RuntimeError: If an unexpected error occurs during the query process.
            ValueError: If the received NTP packet cannot be parsed.
        """
        # Create a UDP socket for communication using a context manager:
        with socket(AF_INET, SOCK_DGRAM) as client:
            # Set the socket timeout to the specified timeout value:
            client.settimeout(self.timeout)

            # Construct an NTP request packet:
            request_packet = bytearray(48)

            # Set the first byte of the request packet to indicate LI=0, VN=3, Mode=3 (client).
            # e.g., LI of 0 means no leap second warning, VN of 3 indicates NTP version 3,
            # and Mode of 3 indicates a client request:
            request_packet[0] = 0x1B  # LI=0, VN=3, Mode=3 (client)

            # Compute and split our local send time into originate timestamp high/low
            # NTP bytes:
            now = time() + NTP_TIMESTAMP_DELTA
            originate_timestamp_high = int(now)
            originate_timestamp_low = int((now - originate_timestamp_high) * 2**32)

            # Overwrite bytes 40–43 and 44–47 with our originate timestamp high/low
            # NTP bytes:
            pack_into("!I", request_packet, 40, originate_timestamp_high)
            pack_into("!I", request_packet, 44, originate_timestamp_low)

            # Send the NTP request packet to the specified endpoint and port:
            client.sendto(request_packet, (self.endpoint, self.port))

            # Receive a response from the endpoint with a buffer size of 1024 bytes:
            data, _ = client.recvfrom(1024)

        try:
            return NTPPacket.from_bytes(data)
        except (ValueError, struct_error) as error:
            raise ValueError("Failed to parse NTP packet") from error


# **************************************************************************************

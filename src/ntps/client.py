# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from socket import AF_INET, SOCK_DGRAM, socket
from struct import error as struct_error

from .packet import NTPPacket

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
            request_packet = b"\x1b" + 47 * b"\0"

            # Send the NTP request packet to the specified endpoint and port:
            client.sendto(request_packet, (self.endpoint, self.port))

            # Receive a response from the endpoint with a buffer size of 1024 bytes:
            data, _ = client.recvfrom(1024)

        try:
            return NTPPacket.from_bytes(data)
        except (ValueError, struct_error) as error:
            raise ValueError("Failed to parse NTP packet") from error


# **************************************************************************************

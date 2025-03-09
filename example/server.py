# **************************************************************************************

# @package        ntps
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from asyncio import CancelledError, get_running_loop, run, sleep
from time import time

from ntps import NTPServer

# **************************************************************************************


# Define a custom NTP server that uses GPS-synced time as the reference time, and a
# stratum level of 0:
class GNSSStratum0NTPServer(NTPServer):
    # Set the reference identifier of the NTP server:
    refid = "GPS"
    # Set the stratum level of the NTP server:
    stratum = 0

    def get_ntp_time(self) -> float:
        # TODO: Replace with actual GPS-synced time retrieval:
        return time()


# **************************************************************************************


async def main() -> None:
    # Retrieve the current running asynchronous event loop:
    loop = get_running_loop()

    server = GNSSStratum0NTPServer()

    # Create a UDP server endpoint on all interfaces at port 123 using your
    # customer implementation (e.g., GNSSStratum0NTPServer):
    transport, _ = await loop.create_datagram_endpoint(
        lambda: server,
        local_addr=server.address,
    )

    # Log that the Stratum 0 NTP Server is running using GPS-synced system time:
    print(
        f"Stratum {server.stratum} NTP Server (using {server.refid} system time) running on UDP port 123"
    )

    try:
        # Maintain the server indefinitely by sleeping in 3600-second intervals:
        while True:
            await sleep(3600)
    except KeyboardInterrupt:
        # Log that a shutdown has been initiated:
        print("Server is gracefully shutting down.")
    except CancelledError:
        # A CancelledError was raised (likely from the sleep task); log a shutdown message:
        print("Server is gracefully shutting down.")
    finally:
        # Close the UDP transport:
        transport.close()


# **************************************************************************************

if __name__ == "__main__":
    run(main())


# **************************************************************************************

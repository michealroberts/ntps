# ntps

Modern, type-safe, zero-dependency python library for implementing a network time protocol (NTP) stratum 0 server.

## Installation

```bash
pip install ntps
```

or

using your preferred environment / package manager of choice, e.g., `poetry`, `conda` or `uv`:

```bash
poetry add ntps
```

```bash
conda install ntps
```

```bash
uv add ntps
```

## Usage

There are two main components in the ntps library: the NTP server and the NTP client.

The NTP server is used to create an NTP server that can be used to synchronize time across a network. The NTP client is used to query an NTP server for the current time.

The following is an example of how to use the ntps library to create an NTP server and client:

### Server

```python
from asyncio import get_running_loop, run
from time import time

from ntps import NTPServer

# Define a custom NTP server that uses GPS-synced time as the reference time, and a
# stratum level of 0:
class GNSSStratum0NTPServer(NTPServer):
    # Set the reference identifier of the NTP server:
    refid = "GPS"
    # Set the stratum level of the NTP server:
    stratum = 0

    def get_ntp_time(self) -> float:
        # Replace this with your actual GPS-synced time retrieval:
        return time()


async def main() -> None:
    # Retrieve the current running asynchronous event loop:
    loop = get_running_loop()

    # Create a UDP server endpoint on all interfaces at port 123 using your
    # custom implementation (e.g., GNSSStratum0NTPServer):
    transport, _ = await loop.create_datagram_endpoint(
        lambda: GNSSStratum0NTPServer(),
        local_addr=('0.0.0.0', 123),
    )
```

### Client

```python
from ntps import NTPClient, NTPPacket

async def main() -> None:
    # Create a new NTP client instance:
    client = NTPClient(endpoint="0.0.0.0", port=123)

    # Send an NTP request to the specified NTP server (e.g., 0.pool.ntp.org):
    packet: NTPPacket = client.query()

    # Print the response packet from the NTP server:
    print(packet)
```

As the ntps instance is fully typed, you can use your IDE's autocompletion to see all the available methods and properties.

We have also provided further usage examples in the [examples](./examples) directory.

## Milestones

- [x] Implement NTP server
- [x] Implement NTP client
- [x] Implement NTP packet
- [ ] Implement kiss-of-death (KoD) packet
- [ ] Implement NTP authentication
- [ ] Implement NTP broadcast
- [ ] Implement NTP multicast
- [ ] Implement NTP symmetric mode

### Miscellaneous

For more information on the NTP protocol, please refer to the [RFC 5905](https://tools.ietf.org/html/rfc5905) document.

### License

This project is licensed under the terms of the MIT license.
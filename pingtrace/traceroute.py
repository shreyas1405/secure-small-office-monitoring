import socket
import time
from typing import List, Dict, Optional


def traceroute_host(dest_name: str, max_hops: int = 30, timeout: float = 2.0) -> List[Dict]:
    """
    Perform a traceroute to dest_name and return a list of hops.
    Each hop is a dict: {"hop": int, "ip": str | None, "rtt_ms": float | None}.
    """
    dest_addr = socket.gethostbyname(dest_name)

    # ICMP socket for receiving Time Exceeded / Destination Unreachable
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    recv_socket.settimeout(timeout)
    recv_socket.bind(("", 0))

    # UDP socket for sending probes
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    port = 33434  # standard traceroute port
    hops: List[Dict] = []

    try:
        for ttl in range(1, max_hops + 1):
            send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            # Clear any stale packets
            # Send probe
            start_time = time.perf_counter_ns()
            send_socket.sendto(b"", (dest_addr, port))

            curr_addr: Optional[str]
            elapsed_ms: Optional[float]

            try:
                _, curr_addr_info = recv_socket.recvfrom(512)
                end_time = time.perf_counter_ns()
                curr_addr = curr_addr_info[0]
                elapsed_ms = (end_time - start_time) / 1e6
            except socket.timeout:
                curr_addr = None
                elapsed_ms = None

            hops.append(
                {
                    "hop": ttl,
                    "ip": curr_addr,
                    "rtt_ms": elapsed_ms,
                }
            )

            if curr_addr == dest_addr:
                break
    finally:
        recv_socket.close()
        send_socket.close()

    return hops

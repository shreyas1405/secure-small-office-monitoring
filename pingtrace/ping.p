from icmplib import ping


def ping_host(host: str, count: int = 4, interval: float = 0.5, timeout: float = 2.0) -> dict:
    """
    Ping a host and return statistics.
    """
    result = ping(
        host,
        count=count,
        interval=interval,
        timeout=timeout,
        privileged=False  # non-root mode on Linux. [web:40][web:74]
    )

    return {
        "host": host,
        "sent": result.packets_sent,
        "received": result.packets_received,
        "packet_loss": result.packet_loss,      # 0.0–1.0 fraction. [web:23]
        "min_rtt": result.min_rtt,              # ms
        "avg_rtt": result.avg_rtt,
        "max_rtt": result.max_rtt,
    }

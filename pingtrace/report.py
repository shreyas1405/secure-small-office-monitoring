import csv
from datetime import datetime
from typing import List, Dict


def write_ping_csv(filename: str, results: List[Dict]) -> None:
    """
    Write ping statistics to a CSV file.
    Each result dict must contain:
    host, sent, received, packet_loss, min_rtt, avg_rtt, max_rtt.
    """
    fieldnames = [
        "timestamp",
        "host",
        "sent",
        "received",
        "packet_loss_percent",
        "min_rtt_ms",
        "avg_rtt_ms",
        "max_rtt_ms",
    ]

    now = datetime.utcnow().isoformat()

    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "timestamp": now,
                "host": r["host"],
                "sent": r["sent"],
                "received": r["received"],
                "packet_loss_percent": r["packet_loss"] * 100.0,
                "min_rtt_ms": r["min_rtt"],
                "avg_rtt_ms": r["avg_rtt"],
                "max_rtt_ms": r["max_rtt"],
            })

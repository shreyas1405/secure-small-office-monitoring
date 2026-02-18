# Secure Small Office Network Monitoring – Technical Documentation

## Table of Contents

1. Architecture Overview
2. System Design
3. Implementation Details
4. Module Breakdown
5. Algorithm Design
6. Data Flow
7. Error Handling
8. Performance Considerations
9. Security Considerations
10. Testing Strategy
11. Future Architecture Enhancements

***

## 1. Architecture Overview

### 1.1 High‑Level Architecture

The project combines a Cisco Packet Tracer **small office network lab** with a **Python-based active monitoring tool** that collects latency and loss statistics, exports them to CSV, and generates HTML reports for analysis.

Conceptual view:

`┌─────────────────────────────────────────────────────┐
│   Small Office Network (Packet Tracer Lab)          │
│                                                     │
│  PCs ─ Switches ─ Router (Inter‑VLAN + ACLs)        │
└───────────────┬─────────────────────────────────────┘
                │  ICMP / traceroute tests
                │
        ┌───────▼─────────────────────────────────────┐
        │   Monitoring Host (Kali / Linux)            │
        │   - nettool.py                              │
        │   - ping / traceroute engine                │
        │   - CSV + HTML reporting                    │
        └───────┬─────────────────────────────────────┘
                │
        ┌───────▼─────────────────────────────────────┐
        │   Reports / Baselines                       │
        │   - baseline_*.csv                          │
        │   - big_report.csv / .html                  │
        │   - report_all.csv / .html                  │
        └─────────────────────────────────────────────┘`

The lab focuses on a **two‑VLAN office** with router‑on‑a‑stick, extended ACLs enforcing one‑way communication, and test PCs that generate realistic ICMP traffic.

### 1.2 Key Components

- **Packet Tracer small office lab**
  - VLAN segmentation (VLAN 10 and 20)
  - Router subinterfaces for inter‑VLAN routing
  - Extended ACL enforcing security policy.

- **Python monitoring tool (`nettool.py`)**
  - ICMP ping statistics (min/avg/max RTT, loss)
  - Traceroute measurements
  - CSV export and HTML report generation.

- **Measurement datasets**
  - Per‑target baselines (`baseline_*.csv`)
  - Aggregated reports (`big_report.csv`, `report_all.csv`, HTML views).

***

## 2. System Design

### 2.1 Network Design

The lab emulates a small office with two departments mapped to VLANs and routed via a single core router using router‑on‑a‑stick.

Topology (simplified):

`┌──────────────────────────────────────┐
│ Router3 (Core)                       │
│  G0/0.10  → VLAN 10  (192.168.10.1)  │
│  G0/0.20  → VLAN 20  (192.168.20.1)  │
└────┬──────────┬──────────────────────┘
     │          │
   Fa0/24     Fa0/24      (trunk links, ACL in path)
     │          │
┌────▼─────┐  ┌─▼────────┐
│ Switch5  │  │ Switch6  │
│ (Core)   │  │ (Access) │
└────┬─────┘  └─┬────────┘
     │          │
   VLAN10     VLAN20
   PC_A       PC_B`

IP addressing model:

| VLAN | Name   | Network          | Gateway       |
|------|--------|------------------|---------------|
| 10   | Dept_A | 192.168.10.0/24  | 192.168.10.1  |
| 20   | Dept_B | 192.168.20.0/24  | 192.168.20.1  |

### 2.2 Security Policy (ACL)

Business rule: **VLAN 10 (Dept_A) may initiate traffic to VLAN 20 (Dept_B), but VLAN 20 must not initiate traffic to VLAN 10**.

Relevant configuration snippet:

```text
ip access-list extended VLAN_INTERVLAN
 deny icmp 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255 echo
 permit icmp any any
 permit ip any any
 !
 interface g0/0.20
  ip access-group VLAN_INTERVLAN in
```

This ACL is applied inbound on the VLAN 20 subinterface so that echo requests from VLAN 20 to VLAN 10 are dropped, while other flows are permitted.

### 2.3 Monitoring Design

The monitoring host (e.g., Kali) runs `nettool.py` and maps lab IPs to real‑world targets for generating realistic latency and loss characteristics:

| Lab Device        | Lab IP        | Real IP (Kali) | Real Target       |
|-------------------|--------------|----------------|-------------------|
| VLAN 10 Gateway   | 192.168.10.1 | 10.0.2.2       | NAT Gateway       |
| VLAN 20 Gateway   | 192.168.20.1 | 1.1.1.1        | Cloudflare DNS    |
| VLAN 20 Host      | 192.168.20.14| 8.8.8.8        | Google DNS        |

This mapping allows you to correlate Packet Tracer logical topology with actual measurement endpoints.

***

## 3. Implementation Details

### 3.1 Monitoring Tool (`nettool.py`)

`nettool.py` is a CLI utility that supports ping measurement, traceroute, CSV export, and HTML report generation.

Typical usage patterns:

```bash
# Basic ping with CSV export
python nettool.py --ping --count 10 --csv report.csv 10.0.2.2 1.1.1.1 8.8.8.8

# Generate HTML report from ping run
python nettool.py --ping --count 10 --csv report.csv --html report.html 10.0.2.2

# Traceroute to multiple hosts
python nettool.py --trace --max-hops 15 --csv trace.csv 8.8.8.8 1.1.1.1
```

The script encapsulates system ping and traceroute calls (or Python equivalents), parses their output, and writes normalized rows to CSV and optional HTML visualizations.

### 3.2 Data Files

Key repository artifacts:

- `small-office-final.pkt` / `small-office-baseline.pkt` / `test11.pkt`
  - Packet Tracer topologies for baseline and scenario testing.

- `baseline_*.csv`
  - Baseline ping measurements for specific targets (e.g., `baseline_1.1.1.1.csv`, `baseline_8.8.8.8.csv`).

- `big_report.csv`, `report_all.csv`
  - Large aggregated measurement runs across multiple hosts and scenarios (e.g., 50 cycles × 3 targets ≈ 150 rows).

- `big_report.html`, `report_all.html`, `baseline_10.0.2.2.html`
  - HTML views summarizing CSV statistics.

- `pingtrace/` or `ping_trace_tool/`
  - Source for the underlying ping/trace logic used by `nettool.py`.

***

## 4. Module Breakdown

### 4.1 `nettool.py` – Main Monitoring Module

- **Argument Parsing**: Uses `argparse` for mode selection (`--ping`, `--trace`) and output control (`--csv`, `--html`).
- **Ping Engine**: Executes ICMP requests, collects RTT stats, and calculates packet loss.
- **Traceroute Engine**: Records path hops, IP addresses, and RTT per hop.
- **Reporting**: Aggregates in-memory data and delegates to CSV/HTML writers.

### 4.2 `pingtrace/` Library

- `ping.py`: Implements low-level ICMP ping logic.
- `traceroute.py`: Implements path discovery logic.
- `report.py`: Handles CSV row writing with timestamped entries.
- `html_report.py`: Generates static HTML dashboard views using the CSV data.

***

## 5. Algorithm Design

### 5.1 Ping Statistics Computation

1.  **Initialize**: Set counters for `sent=0`, `received=0`, `rtt_list=[]`.
2.  **Loop**: For `count` iterations:
    - Send ICMP Echo Request.
    - If Echo Reply received:
        - Increment `received`.
        - Calculate RTT (Reply Time - Send Time).
        - Append to `rtt_list`.
3.  **Finalize**:
    - `loss_percent = (sent - received) / sent * 100`.
    - `min_rtt = min(rtt_list)`, `avg_rtt = mean(rtt_list)`, `max_rtt = max(rtt_list)`.

***

## 6. Data Flow

1.  **Input**: User IP targets (e.g., `8.8.8.8`) passed via CLI.
2.  **Execution**: `nettool.py` calls `ping_host()` for each target.
3.  **Storage**: Statistics objects are passed to `write_ping_csv()`.
4.  **Reporting**: `generate_html_report()` reads the CSV and produces a `.html` file.
5.  **Output**: CSV/HTML files persisted to the local directory for Git tracking.

***

## 7. Error Handling

- **Timeouts**: If a host is unreachable (e.g., link down scenario), the tool records 100% loss and N/A for RTT.
- **Permissions**: Ping requires raw socket permissions on some OSs; the tool handles exceptions if execution fails due to lack of privileges.
- **File I/O**: Validates presence of `--csv` flag when `--html` is requested to prevent data source errors.

***

## 8. Performance Considerations

- **Sequential Processing**: Hosts are pinged one by one. For large target lists, execution time is `num_hosts * count * timeout`.
- **Lightweight Reporting**: CSV and HTML generation is performed in-memory after all pings complete to avoid excessive disk I/O during measurement.

***

## 9. Security Considerations

- **ACL Verification**: The primary security goal is verifying that the `VLAN_INTERVLAN` ACL correctly drops unauthorized pings while allowing valid flows.
- **Least Privilege**: The Packet Tracer lab demonstrates "deny by default" for specific inter-VLAN flows, a core security principle.

***

## 10. Testing Strategy

- **Scenario A: Baseline**: Normal operation, all VLANs communicate.
- **Scenario B: Security (ACL)**: Apply ACL and verify VLAN 20 → VLAN 10 is blocked (100% loss).
- **Scenario C: Failure**: Shut down router interfaces and verify total connectivity loss (100% loss for all).

***

## 11. Future Architecture Enhancements

- **Redundancy**: Implementation of HSRP/VRRP for gateway high availability.
- **Automation**: Scheduling `nettool.py` via cron for continuous baseline collection.
- **Integration**: Exporting metrics to a centralized dashboard like Grafana.

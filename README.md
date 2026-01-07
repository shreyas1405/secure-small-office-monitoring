# Secure Small Office Network Monitoring

[![GitHub](https://img.shields.io/badge/GitHub-shreyas1405-181717?logo=github)](https://github.com/shreyas1405) [![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

A comprehensive **final-year project** demonstrating design, implementation, and monitoring of a secure small office network using Cisco Packet Tracer with VLAN segmentation, inter-VLAN routing, and network access control policies (ACLs). Includes a custom Python-based monitoring tool for active network measurements.

## Project Highlights

✅ **Multi-VLAN Network Design** - Department-level segregation with VLAN 10 (Dept_A) and VLAN 20 (Dept_B)  
✅ **Router-on-a-Stick Architecture** - Single router managing multiple VLANs via subinterfaces  
✅ **Security Enforcement** - Extended ACLs enforcing one-way traffic restrictions  
✅ **Active Monitoring** - Python ping-trace tool measuring latency and packet loss  
✅ **Real-World Simulation** - Packet Tracer topology + Kali Linux monitoring integration  
✅ **Comprehensive Testing** - Baseline, security, and failure scenarios documented  

## Network Topology

```
┌──────────────────────────────────────┐
│      Router3 (Core)                  │
│  G0/0.10      │      G0/0.20         │
│  192.168.10.1 │ 192.168.20.1        │
└────┬──────────┬──────────────────────┘
     │          │ (ACL Applied)
  Fa0/24      Fa0/24
     │          │
 ┌───┴──────────┴────────┐
 │   Switch5 (Core)      │
 │   Fa0/23 ↔ Switch6    │
 └───┬────────────────────┘
     │ Trunk
 ┌───┴────────────┐
 │  Switch6       │
 │  (Access)      │
 └───┬────────┬───┘
     │        │
  VLAN10   VLAN20
  PC_A      PC_B
192.168.10.11 192.168.20.14
```

## IP Addressing

| VLAN | Name | Network | Gateway |
|------|------|---------|----------|
| 10 | Dept_A | 192.168.10.0/24 | 192.168.10.1 |
| 20 | Dept_B | 192.168.20.0/24 | 192.168.20.1 |

## Key Features

### Security - ACL Implementation

**Policy:** Block VLAN 20 → VLAN 10 while allowing VLAN 10 → VLAN 20

```
ip access-list extended VLAN_INTERVLAN
 deny   icmp 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255 echo
 permit icmp any any
 permit ip any any
!
interface g0/0.20
 ip access-group VLAN_INTERVLAN in
```

### Test Results

| Scenario | VLAN 10→20 | VLAN 20→10 | Packet Loss | RTT (Local) |
|----------|-----------|-----------|-------------|-------------|
| Baseline | ✓ | ✓ | 0% | 0.6ms |
| With ACL | ✓ | ✗ | 0% | 0.6ms |
| Link Down | ✗ | ✗ | 100% | N/A |

## Monitoring Tool Usage

```bash
# Basic ping with CSV export
python nettool.py --ping --count 10 --csv report.csv 10.0.2.2 1.1.1.1 8.8.8.8

# Generate HTML report
python nettool.py --ping --count 10 --csv report.csv --html report.html 10.0.2.2

# Traceroute to multiple hosts
python nettool.py --trace --max-hops 15 --csv trace.csv 8.8.8.8 1.1.1.1
```

## Repository Files

- **small-office-final.pkt** - Main Packet Tracer topology
- **nettool.py** - Python monitoring tool
- **big_report.csv** - 150 rows of measurement data (50 cycles × 3 targets)
- **big_report.html** - HTML visualization
- **baseline_*.csv** - Individual scenario measurements
- **ping_trace_tool/** - Tool source code

## IP Mapping (Packet Tracer ↔ Real Measurements)

| Lab Device | Lab IP | Real IP (Kali) | Real Target |
|---|---|---|---|
| VLAN 10 Gateway | 192.168.10.1 | 10.0.2.2 | NAT Gateway |
| VLAN 20 Gateway | 192.168.20.1 | 1.1.1.1 | Cloudflare DNS |
| VLAN 20 Host | 192.168.20.14 | 8.8.8.8 | Google DNS |

## Sample Monitoring Output

```
destination_ip,sent,received,loss_percent,rtt_min_ms,rtt_avg_ms,rtt_max_ms
10.0.2.2,10,10,0,0.307,0.605,0.991
1.1.1.1,10,10,0,50.511,66.611,98.786
8.8.8.8,10,10,0,47.885,83.354,102.100
```

## Technical Skills Demonstrated

✓ Cisco Networking (VLANs, trunking, subinterfaces)  
✓ Access Control Lists (ACLs) and firewall policies  
✓ Network topology design and implementation  
✓ Python automation and network tools development  
✓ Data analysis (CSV/HTML reporting)  
✓ Active network monitoring (ICMP, traceroute)  
✓ Virtualization and virtual networking  
✓ Git version control and documentation  

## Installation

```bash
git clone https://github.com/shreyas1405/secure-small-office-monitoring.git
cd secure-small-office-monitoring
cd ping_trace_tool
pip install -r requirements.txt
cd ..
python nettool.py --ping --count 20 --csv results.csv 10.0.2.2 1.1.1.1 8.8.8.8
```

## Future Enhancements

- [ ] HSRP (Hot Standby Router Protocol) for redundancy
- [ ] QoS (Quality of Service) policies
- [ ] Snort/Suricata IDS integration
- [ ] pfSense firewall implementation
- [ ] SNMP monitoring for switches
- [ ] Syslog centralization
- [ ] Wireless network extension
- [ ] Load balancing

## Project Statistics

- **Network Devices:** 1 Router + 2 Switches + 4 PCs
- **VLANs:** 2 (Dept_A, Dept_B)
- **Security Policies:** 1 Extended ACL
- **Test Scenarios:** 3 (Baseline, ACL, Failure)
- **Data Points:** 150+ measurements
- **Code Lines:** 500+ (Python)
- **Documentation:** 4+ pages

## Author

**Shreyas** - CSE Final Year Student  
**Institution:** SJBIT, Bengaluru  
**Date:** January 2026  
**GitHub:** [@shreyas1405](https://github.com/shreyas1405)

## License

MIT License - see LICENSE file for details

---

**Last Updated:** January 7, 2026

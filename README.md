# Custom Traceroute Implementation

A Python implementation of the `traceroute` network diagnostic tool using Scapy, created as part of CSSE 341 Lab 02.

## Overview

This project reverse-engineers and reimplements the Unix `traceroute` utility to discover the network path between a source and destination. It involves understanding of IP and ICMP protocols, particularly TTL manipulation and ICMP message types.

## How It Works

Traceroute discovers network hops by exploiting the Time-To-Live (TTL) field in IP packets:

1. **Send UDP packets with incrementing TTL values** (starting from 1)
2. **Each router decrements TTL by 1** as the packet passes through
3. **When TTL reaches 0**, the router drops the packet and sends back an **ICMP Time Exceeded (Type 11)** message
4. **Record the router's IP address** from the ICMP response
5. **Final destination** responds with **ICMP Destination Unreachable - Port Unreachable (Type 3)** when the UDP packet arrives
6. **Repeat** for TTL=1, 2, 3... until reaching the destination

### Why 3 Packets Per Hop?

- Provides **redundancy** against packet loss
- Enables **round-trip time (RTT) measurements** for latency analysis
- Helps identify **network variability**

## Requirements

- Python 3.x
- Scapy library (pre-installed in lab containers)
- Root/sudo privileges (for raw socket access)

## Usage
```bash
# Make executable
chmod +x my_traceroute.py

# Trace route to a destination
sudo ./my_traceroute.py <destination>

# Examples
sudo ./my_traceroute.py 1.1.1.1
sudo ./my_traceroute.py google.com
sudo ./my_traceroute.py hostB
```

## Example Output
```
$ sudo ./my_traceroute.py 1.1.1.1
traceroute to 1.1.1.1, 30 hops max
 1  10.10.0.1  91.238 ms  43.831 ms  47.817 ms
 2  137.112.104.3  47.687 ms  43.946 ms  35.813 ms
 3  137.112.9.156  35.880 ms  31.852 ms  47.888 ms
 4  *  *  *
 5  199.8.48.102  31.807 ms  31.896 ms  31.865 ms
 6  199.8.220.1  31.866 ms  31.859 ms  31.894 ms
 7  206.53.139.34  43.831 ms  43.900 ms  35.846 ms
 8  1.1.1.1  31.870 ms  31.891 ms  35.846 ms
```

## Technical Details

### Packet Structure

Each packet consists of:
- **IP Layer**: Destination address and TTL value
- **UDP Layer**: High port number (33434) that's typically closed

### ICMP Response Types

- **Type 11 (Time Exceeded)**: Intermediate router, TTL expired
- **Type 3 (Destination Unreachable)**: Final destination reached
- **No response (*)**: Router doesn't send ICMP, or packet was dropped

### Key Implementation Features

- Configurable maximum hops (default: 30)
- Configurable number of packets per hop (default: 3)
- 2-second timeout per packet
- RTT measurement in milliseconds
- Handles timeouts gracefully with `*` markers

## Lab Environment

This implementation was developed and tested in a Docker-based network environment with:
- **hostA** (10.10.0.4): Source machine
- **hostB** (10.10.0.5): Test destination on local network
- **attacker** (10.10.0.13): Additional test machine

## Comparison with Standard Traceroute

This implementation uses UDP packets (like Unix `traceroute`). Windows `tracert` uses ICMP Echo Request instead. Both achieve the same goal through different protocols.

## Limitations

- Requires root/sudo privileges
- Some routers/firewalls don't respond to ICMP Time Exceeded
- Network paths can change during execution
- UDP implementation only (no ICMP variant)

## Course Information

- **Course**: CSSE 341 - Computer Networks and Network Security
- **Institution**: Rose-Hulman Institute of Technology
- **Lab**: Lab 02 - ICMP and Traceroute

## References

- [Scapy Documentation](https://scapy.readthedocs.io/)
- RFC 792 - Internet Control Message Protocol (ICMP)
- RFC 768 - User Datagram Protocol (UDP)

## License

Academic project - Rose-Hulman Institute of Technology

---

*Note: This is an educational implementation. For production use, consider the standard `traceroute` utility.*

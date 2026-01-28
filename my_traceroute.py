#!/usr/bin/env python3
from scapy.all import *
from scapy.layers.inet import IP, UDP, ICMP
import sys
import time

def traceroute(destination, max_hops=30, num_packets=3):
    print(f"traceroute to {destination}, {max_hops} hops max")
    
    for ttl in range(1, max_hops + 1):
        hop_info = []
        reached_destination = False
        
        for i in range(num_packets):
            # create packet with specific TTL
            packet = IP(dst=destination, ttl=ttl) / UDP(dport=33434)
            
            # send and wait for response
            start_time = time.time()
            response = sr1(packet, verbose=0, timeout=2)
            rtt = (time.time() - start_time) * 1000
            
            if response is None:
                hop_info.append(('*', None))
            else:
                source_ip = response[IP].src
                hop_info.append((source_ip, rtt))
                
                # check if we reached destination
                if response.haslayer(ICMP) and response[ICMP].type == 3:
                    reached_destination = True
        
        # print hop information
        ips = [ip for ip, rtt in hop_info if ip != '*']
        if ips:
            print(f" {ttl}  {ips[0]}", end='')
        else:
            print(f" {ttl}  *", end='')
        
        for ip, rtt in hop_info:
            if rtt is not None:
                print(f"  {rtt:.3f} ms", end='')
            else:
                print("  *", end='')
        print()
        
        if reached_destination:
            break

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./my_traceroute.py <destination>")
        sys.exit(1)
    
    traceroute(sys.argv[1])

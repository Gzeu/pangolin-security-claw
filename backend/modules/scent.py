from scapy.all import srp, Ether, ARP
import random

def scan_network(ip_range: str):
    print(f"[SCENT] Sniffing network: {ip_range}")
    devices = []
    for i in range(1, 6):
        scent_level = random.randint(10, 100) 
        devices.append({
            "ip": f"192.168.1.{100+i}",
            "mac": f"00:1A:2B:3C:4D:{10+i}",
            "scent_level": scent_level
        })
    return devices
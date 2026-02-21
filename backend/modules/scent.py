from scapy.all import srp, Ether, ARP
import socket
import struct

def get_default_gateway_ip():
    """Attempt to find the default gateway to guess the local subnet."""
    try:
        # A simple hack to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "192.168.1.1"

def scan_network(ip_range: str = None):
    """
    Discovers devices on the network using actual ARP packets.
    Requires Root/Administrator privileges to execute successfully.
    """
    if not ip_range:
        local_ip = get_default_gateway_ip()
        # Create a simple /24 subnet string based on local IP
        ip_range = f"{local_ip.rsplit('.', 1)[0]}.0/24"
        
    print(f"[SCENT] Sniffing network with Scapy on subnet: {ip_range}")
    devices = []

    try:
        # Create an ARP request packet
        arp_request = ARP(pdst=ip_range)
        # Create an Ethernet frame directed to the broadcast MAC address
        broadcast_ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        # Combine the Ethernet frame and ARP request
        packet = broadcast_ether / arp_request

        # Send the packet and receive responses
        # timeout controls how long to wait for a response
        answered, _ = srp(packet, timeout=2, verbose=0)

        for sent, received in answered:
            # Scent level calculation is simplified here.
            # In a real IPS, it would compare MACs against a known/trusted list.
            # Here we assign a baseline threat level based on the fact it's an unknown device.
            scent_level = 50 
            
            # If the IP ends in .1, it's usually the router, mark as lower threat
            if received.psrc.endswith(".1"):
                scent_level = 10
                
            devices.append({
                "ip": received.psrc,
                "mac": received.hwsrc,
                "scent_level": scent_level
            })
            
    except PermissionError:
        print("[ERROR] Scapy requires Root/Administrator privileges to send ARP packets.")
        # Fallback to simulated data if permissions fail, so the UI doesn't break entirely
        print("[SCENT] Falling back to simulated network data...")
        return [
            {"ip": "192.168.1.1", "mac": "00:11:22:33:44:55", "scent_level": 10},
            {"ip": "192.168.1.104", "mac": "AA:BB:CC:DD:EE:FF", "scent_level": 40},
            {"ip": "ERROR_NO_ROOT", "mac": "Permission Denied", "scent_level": 100}
        ]
    except Exception as e:
         print(f"[ERROR] Network scan failed: {e}")

    return devices
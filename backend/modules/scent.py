import subprocess
import socket
import platform
import re

def get_local_subnet():
    """Detect the local machine's IP to determine the /24 subnet."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        subnet = ip.rsplit('.', 1)[0]
        return subnet, ip
    except Exception:
        return "192.168.1", "192.168.1.1"

def parse_arp_table():
    """
    Reads the system ARP cache using the native 'arp' command.
    No third-party library required. Works on Linux, macOS, and Windows.
    Uses stdlib subprocess with a strict allowlist — no shell=True.
    """
    system = platform.system()
    devices = []

    try:
        # SECURITY: Never use shell=True. Pass args as a list.
        if system == "Windows":
            cmd = ["arp", "-a"]
        else:
            # Linux/macOS
            cmd = ["arp", "-n"]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,    # Prevent hanging
            shell=False    # SECURITY: shell=False prevents injection
        )
        output = result.stdout
        
        # Regex to extract IP and MAC from the arp table output
        ip_mac_pattern = re.compile(
            r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+[\w:()\-]+\s+([0-9a-fA-F:]{11,17})"
        )
        
        for match in ip_mac_pattern.finditer(output):
            ip = match.group(1)
            mac = match.group(2)
            # Assign threat level: router (.1) is trusted, rest are unknown
            scent_level = 10 if ip.endswith(".1") else 50
            devices.append({"ip": ip, "mac": mac, "scent_level": scent_level})
            
    except FileNotFoundError:
        print("[SCENT] 'arp' command not found on this system.")
    except subprocess.TimeoutExpired:
        print("[SCENT] ARP scan timed out.")
    except Exception as e:
        print(f"[SCENT] Error reading ARP table: {e}")

    return devices

def scan_network():
    """
    Returns devices discovered from the system ARP table.
    No root privileges required. No raw packet injection.
    Pure stdlib: subprocess + socket + re.
    """
    subnet, local_ip = get_local_subnet()
    print(f"[SCENT] Reading ARP table for subnet: {subnet}.0/24")
    devices = parse_arp_table()
    print(f"[SCENT] Found {len(devices)} devices.")
    return devices

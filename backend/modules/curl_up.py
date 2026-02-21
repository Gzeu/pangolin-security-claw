import psutil
import time

WHITELIST = ["System", "svchost.exe", "explorer.exe", "python.exe", "node"]

def trigger_curl_up(proc):
    try:
        print(f"[CURL-UP] Threat detected: {proc.name()} (PID: {proc.pid}).")
        proc.suspend() 
        print(f"[CURL-UP] Process suspended. Network ports theoretically blocked for PID {proc.pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
        print(f"[ERROR] Could not quarantine process: {e}")

def monitor_processes():
    print("Pangolin Watchdog activated. Monitoring CPU...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu_usage = proc.cpu_percent(interval=0.1)
            if cpu_usage > 80.0 and proc.info['name'] not in WHITELIST:
                trigger_curl_up(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
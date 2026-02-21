import psutil
import time

WHITELIST = ["System", "svchost.exe", "explorer.exe", "python.exe", "node"]

def trigger_curl_up(proc):
    try:
        print(f"[CURL-UP] Threat detected: {proc.name()} (PID: {proc.pid}).")
        
        # [*** WEAKNESS: RACE CONDITION / TOCTOU ***]
        # Time-of-check to time-of-use vulnerability. The process might have terminated 
        # naturally between the CPU check and this suspend call, raising an exception.
        proc.suspend() 
        print(f"[CURL-UP] Process suspended. Network ports theoretically blocked for PID {proc.pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
        print(f"[ERROR] Could not quarantine process: {e}")

def monitor_processes():
    print("Pangolin Watchdog activated. Monitoring CPU...")
    # [*** WEAKNESS: SINGLE EXECUTION LOOP ***]
    # Currently, this only scans once when the API is hit. 
    # A real watchdog needs a `while True:` loop with a `time.sleep(x)` to run continuously.
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # [*** WEAKNESS: BLOCKING CALL ***]
            # `interval=0.1` blocks the thread for 0.1s per process. 
            # If there are 300 processes, one full scan takes 30 seconds. 
            # This should be asynchronous or use `interval=None` (non-blocking) and compare states later.
            cpu_usage = proc.cpu_percent(interval=0.1)
            
            # [*** VULNERABILITY: WHITELIST BYPASS ***]
            # The whitelist relies on exact string matching of `proc.info['name']`.
            # Malware can easily rename its executable to `svchost.exe` or `python.exe` to bypass this check entirely.
            # Fix: Check the executable path (e.g., `C:\Windows\System32\svchost.exe`) or verify digital signatures.
            if cpu_usage > 80.0 and proc.info['name'] not in WHITELIST:
                trigger_curl_up(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
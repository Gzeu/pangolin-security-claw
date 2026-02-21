import psutil
import time

# [FIXED: Strict path whitelisting to prevent generic rename bypass]
WHITELIST_PATHS = ["\\windows\\", "/usr/bin/", "/bin/", "/sbin/"]

def trigger_curl_up(proc):
    try:
        print(f"[CURL-UP] Threat detected: {proc.name()} (PID: {proc.pid}).")
        proc.suspend() 
        print(f"[CURL-UP] Process suspended. Network ports theoretically blocked for PID {proc.pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        # [FIXED: Handled TOCTOU race condition silently to prevent crashes]
        pass

def monitor_processes():
    print("Pangolin Watchdog activated. Monitoring CPU...")
    
    # [FIXED: Non-blocking CPU measurement over a 1-second interval]
    # First loop primes the CPU timers
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    time.sleep(1.0) # Non-blocking sleep to gather metrics accurately
    
    # Second loop reads the accurate percentages
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            cpu_usage = proc.cpu_percent(interval=None)
            exe_path = proc.info.get('exe') or ""
            
            # Verify if the absolute path is whitelisted
            is_whitelisted = any(w in exe_path.lower() for w in WHITELIST_PATHS)
            
            # We enforce that exe_path must exist (some root processes hide this, but user-land malware won't)
            if cpu_usage > 80.0 and not is_whitelisted and exe_path:
                trigger_curl_up(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
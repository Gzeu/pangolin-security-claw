import psutil
import time

WHITELIST_PATHS = ["\\windows\\", "/usr/bin/", "/bin/", "/sbin/"]

def trigger_curl_up(proc):
    try:
        print(f"[CURL-UP] Threat detected: {proc.name()} (PID: {proc.pid}).")
        proc.suspend() 
        print(f"[CURL-UP] Process suspended. Network ports theoretically blocked for PID {proc.pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

def monitor_processes():
    print("Pangolin Watchdog activated. Monitoring CPU...")
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    time.sleep(1.0) 
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            cpu_usage = proc.cpu_percent(interval=None)
            exe_path = proc.info.get('exe') or ""
            
            is_whitelisted = any(w in exe_path.lower() for w in WHITELIST_PATHS)
            
            if cpu_usage > 80.0 and not is_whitelisted and exe_path:
                trigger_curl_up(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
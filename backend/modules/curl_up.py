import psutil
import time

WHITELIST = ["System", "svchost.exe", "explorer.exe", "python.exe", "node"]

def trigger_curl_up(proc):
    try:
        print(f"[CURL-UP] Amenintare detectata: {proc.name()} (PID: {proc.pid}).")
        proc.suspend() 
        print(f"[CURL-UP] Proces suspendat. Porturi de retea blocate teoretic pentru PID {proc.pid}.")
    except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
        print(f"[EROARE] Nu s-a putut carantina procesul: {e}")

def monitor_processes():
    print("Pangolin Watchdog activat. Monitorizare CPU...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu_usage = proc.cpu_percent(interval=0.1)
            if cpu_usage > 80.0 and proc.info['name'] not in WHITELIST:
                trigger_curl_up(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
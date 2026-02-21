from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from modules.curl_up import monitor_processes
from modules.scent import scan_network

app = FastAPI(title="Pangolin-Guard OS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scent/scan")
def trigger_scent():
    results = scan_network("192.168.1.0/24")
    return {"status": "SUCCESS", "devices": results}

@app.post("/api/curl-up/activate")
def activate_curl_up(background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_processes)
    return {"status": "ARMORED", "message": "Pangolin a intrat in modul defensiv (Curl-Up)."}
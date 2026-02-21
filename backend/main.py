from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from modules.curl_up import monitor_processes
from modules.scent import scan_network
from modules.scales import encrypt_file_scales
from modules.long_tongue import search_leaks

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
    return {"status": "ARMORED", "message": "Pangolin entered defensive mode (Curl-Up)."}

@app.post("/api/scales/encrypt")
def trigger_scales(file_path: str = "default_document.txt"):
    result = encrypt_file_scales(file_path)
    return {"status": "ENCRYPTED", "details": result}

@app.get("/api/long-tongue/search")
def trigger_long_tongue(query: str):
    results = search_leaks(query)
    return {"status": "SUCCESS", "leaks": results}
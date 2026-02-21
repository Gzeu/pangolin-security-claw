from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from modules.curl_up import monitor_processes
from modules.scent import scan_network
from modules.scales import encrypt_file_scales, decrypt_file_scales
from modules.long_tongue import search_leaks
from database import init_db, get_connection
import uuid
import os
import shutil

init_db()

app = FastAPI(title="Pangolin-Guard OS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   
        "http://localhost:3000",   
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/api/scent/scan")
def trigger_scent():
    results = scan_network()
    conn = get_connection()
    conn.execute("DELETE FROM threat_radar")
    
    for dev in results:
        conn.execute(
            "INSERT INTO threat_radar (id, entity_type, identifier, scent_level) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), "NETWORK_DEVICE", dev["ip"], dev["scent_level"])
        )
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "devices": results}

@app.post("/api/curl-up/activate")
def activate_curl_up(background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_processes)
    return {"status": "ARMORED", "message": "Pangolin entered defensive mode (Curl-Up)."}

@app.post("/api/scales/encrypt")
def trigger_scales_encrypt(file: UploadFile = File(...)):
    safe_filename = f"{uuid.uuid4().hex[:8]}_{os.path.basename(file.filename)}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    result = encrypt_file_scales(file_path)
    
    if result.get("status") == "ERROR":
         return result
         
    conn = get_connection()
    conn.execute(
        "INSERT INTO encrypted_scales (id, filename, total_chunks, status) VALUES (?, ?, ?, ?)",
        (str(uuid.uuid4()), safe_filename, result["total_scales"], "ARMORED")
    )
    conn.commit()
    conn.close()
    return {"status": "ENCRYPTED", "details": result}

@app.post("/api/scales/decrypt")
def trigger_scales_decrypt(file: UploadFile = File(...)):
    safe_filename = f"{uuid.uuid4().hex[:8]}_{os.path.basename(file.filename)}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    result = decrypt_file_scales(file_path)
    
    if result.get("status") == "ERROR":
         return result
         
    conn = get_connection()
    original_name = file.filename[:-9] if file.filename.endswith(".pangolin") else file.filename
    conn.execute(
        "UPDATE encrypted_scales SET status = 'UNROLLED' WHERE filename LIKE ?",
        (f"%{original_name}%",) 
    )
    conn.commit()
    conn.close()
    return {"status": "UNROLLED", "details": result}

@app.get("/api/long-tongue/search")
def trigger_long_tongue(directory: str = "."):
    safe_dir = os.path.normpath(os.path.join(os.getcwd(), directory))
    if not safe_dir.startswith(os.getcwd()):
        return {"status": "ERROR", "message": "Path traversal attempt detected and blocked."}
    results = search_leaks(safe_dir)
    
    conn = get_connection()
    conn.execute("DELETE FROM data_leaks")
    
    for leak in results:
        conn.execute(
            "INSERT INTO data_leaks (id, file_path, leak_type, confidence_score) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), leak["file"], leak["leak_type"], leak["confidence_score"])
        )
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "leaks": results}
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from modules.curl_up import monitor_processes
from modules.scent import scan_network
from modules.scales import encrypt_file_scales
from modules.long_tongue import search_leaks
from database import init_db, get_connection
import uuid

# Initialize the SQLite database tables on startup
init_db()

app = FastAPI(title="Pangolin-Guard OS API")

# SECURITY: Restrict CORS to localhost only.
# Never use allow_origins=["*"] in a security tool.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # fallback CRA dev server
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/api/scent/scan")
def trigger_scent():
    results = scan_network()
    conn = get_connection()
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
def trigger_scales(file_path: str = "default_document.txt"):
    # SECURITY: Sanitize file path to prevent path traversal attacks
    import os
    safe_path = os.path.normpath(os.path.join(os.getcwd(), file_path))
    if not safe_path.startswith(os.getcwd()):
        return {"status": "ERROR", "message": "Path traversal attempt detected and blocked."}
    result = encrypt_file_scales(safe_path)
    conn = get_connection()
    conn.execute(
        "INSERT INTO encrypted_scales (id, filename, total_chunks, status) VALUES (?, ?, ?, ?)",
        (str(uuid.uuid4()), file_path, result["total_scales"], "ARMORED")
    )
    conn.commit()
    conn.close()
    return {"status": "ENCRYPTED", "details": result}

@app.get("/api/long-tongue/search")
def trigger_long_tongue(directory: str = "."):
    # SECURITY: Sanitize directory path to prevent path traversal
    import os
    safe_dir = os.path.normpath(os.path.join(os.getcwd(), directory))
    if not safe_dir.startswith(os.getcwd()):
        return {"status": "ERROR", "message": "Path traversal attempt detected and blocked."}
    results = search_leaks(safe_dir)
    conn = get_connection()
    for leak in results:
        conn.execute(
            "INSERT INTO data_leaks (id, file_path, leak_type, confidence_score) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), leak["file"], leak["leak_type"], leak["confidence_score"])
        )
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "leaks": results}

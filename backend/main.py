from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from modules.curl_up import monitor_processes
from modules.scent import scan_network
from modules.scales import encrypt_file_scales
from modules.long_tongue import search_leaks
import models
from database import engine, get_db

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pangolin-Guard OS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scent/scan")
def trigger_scent(db: Session = Depends(get_db)):
    results = scan_network("192.168.1.0/24")
    # Save to DB
    for dev in results:
        db_threat = models.ThreatRadar(
            entity_type="NETWORK_DEVICE",
            identifier=dev["ip"],
            scent_level=dev["scent_level"]
        )
        db.add(db_threat)
    db.commit()
    return {"status": "SUCCESS", "devices": results}

@app.post("/api/curl-up/activate")
def activate_curl_up(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Passing DB session is complex for background tasks without scope management, 
    # keeping it simple for now. The watchdog will log to DB internally in the future.
    background_tasks.add_task(monitor_processes)
    return {"status": "ARMORED", "message": "Pangolin entered defensive mode (Curl-Up)."}

@app.post("/api/scales/encrypt")
def trigger_scales(file_path: str = "default_document.txt", db: Session = Depends(get_db)):
    result = encrypt_file_scales(file_path)
    # Save to DB
    db_scale = models.EncryptedScale(
        original_filename=file_path,
        total_chunks=result["total_scales"],
        encryption_status="ARMORED"
    )
    db.add(db_scale)
    db.commit()
    return {"status": "ENCRYPTED", "details": result}

@app.get("/api/long-tongue/search")
def trigger_long_tongue(query: str, db: Session = Depends(get_db)):
    results = search_leaks(query)
    # Save to DB
    for leak in results:
        db_leak = models.DataLeak(
            file_path=leak["file"],
            leak_type=leak["leak_type"],
            confidence_score=leak["confidence_score"]
        )
        db.add(db_leak)
    db.commit()
    return {"status": "SUCCESS", "leaks": results}
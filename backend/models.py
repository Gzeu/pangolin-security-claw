from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
import datetime
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class EncryptedScale(Base):
    __tablename__ = "encrypted_scales"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    original_filename = Column(String, index=True)
    total_chunks = Column(Integer)
    encryption_status = Column(String, default="ARMORED")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ThreatRadar(Base):
    __tablename__ = "threat_radar"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    entity_type = Column(String) # 'PROCESS' or 'NETWORK_DEVICE'
    identifier = Column(String, index=True) # PID or IP/MAC
    scent_level = Column(Integer, default=0)
    cpu_usage = Column(Float, nullable=True)
    status = Column(String, default="ACTIVE") # 'ACTIVE', 'QUARANTINED', 'BLOCKED'
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

class DataLeak(Base):
    __tablename__ = "data_leaks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    file_path = Column(String, index=True)
    leak_type = Column(String)
    confidence_score = Column(Float)
    resolved = Column(Boolean, default=False)
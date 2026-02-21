import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2, HKDF
from Crypto.Hash import SHA256

CHUNK_SIZE = 1024 * 64  
MAX_CHUNK_READ = CHUNK_SIZE + 64 

def secure_delete(file_path: str):
    """Overwrites file with random bytes before deletion to prevent forensic recovery."""
    try:
        length = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            f.write(os.urandom(length))
        os.remove(file_path)
    except Exception:
        pass 

def encrypt_file_scales(file_path: str, password: str = "PangolinStrong123!"):
    if not os.path.exists(file_path):
        return {"status": "ERROR", "message": "File not found."}

    print(f"[SCALES] Applying armored scales to: {file_path}")
    output_path = f"{file_path}.pangolin"
    
    salt = get_random_bytes(16)
    master_key = PBKDF2(password, salt, 32, count=200000, hmac_hash_module=SHA256)
    
    total_chunks = 0
    encrypted_scales_meta = []

    try:
        with open(file_path, "rb") as infile, open(output_path, "wb") as outfile:
            outfile.write(b"PANGOLIN_V2")
            outfile.write(salt)
            
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                layer_key = HKDF(master_key, 32, salt=salt, context=str(total_chunks).encode(), hashmod=SHA256)
                cipher = AES.new(layer_key, AES.MODE_GCM)
                
                ciphertext, tag = cipher.encrypt_and_digest(chunk)
                
                outfile.write(len(cipher.nonce).to_bytes(4, 'little'))
                outfile.write(cipher.nonce)
                outfile.write(len(tag).to_bytes(4, 'little'))
                outfile.write(tag)
                outfile.write(len(ciphertext).to_bytes(4, 'little'))
                outfile.write(ciphertext)
                
                encrypted_scales_meta.append({
                    "scale_id": total_chunks,
                    "nonce": cipher.nonce.hex(),
                    "status": "ARMORED"
                })
                total_chunks += 1
                
        secure_delete(file_path)
                
    except Exception as e:
        print(f"[SCALES] Encryption error: {e}")
        return {"status": "ERROR", "message": str(e)}

    return {
        "file": output_path,
        "original_file": file_path,
        "total_scales": total_chunks,
        "scales_data": encrypted_scales_meta,
        "status": "ARMORED"
    }

def decrypt_file_scales(encrypted_file_path: str, password: str = "PangolinStrong123!"):
    if not os.path.exists(encrypted_file_path) or not encrypted_file_path.endswith(".pangolin"):
        return {"status": "ERROR", "message": "Invalid or missing .pangolin file."}

    print(f"[SCALES] Unrolling scales for: {encrypted_file_path}")
    output_path = encrypted_file_path[:-9]
    
    try:
        with open(encrypted_file_path, "rb") as infile, open(output_path, "wb") as outfile:
            header = infile.read(11)
            if header != b"PANGOLIN_V2":
                 return {"status": "ERROR", "message": "Invalid file format or outdated version."}
                 
            salt = infile.read(16)
            master_key = PBKDF2(password, salt, 32, count=200000, hmac_hash_module=SHA256)
            total_chunks = 0
            
            while True:
                nonce_len_bytes = infile.read(4)
                if not nonce_len_bytes:
                    break 
                nonce_len = int.from_bytes(nonce_len_bytes, 'little')
                nonce = infile.read(nonce_len)
                
                tag_len_bytes = infile.read(4)
                tag_len = int.from_bytes(tag_len_bytes, 'little')
                tag = infile.read(tag_len)
                
                ct_len_bytes = infile.read(4)
                ct_len = int.from_bytes(ct_len_bytes, 'little')
                
                if ct_len > MAX_CHUNK_READ:
                    return {"status": "ERROR", "message": "File corruption detected. Chunk exceeds memory limits."}
                    
                ciphertext = infile.read(ct_len)
                
                layer_key = HKDF(master_key, 32, salt=salt, context=str(total_chunks).encode(), hashmod=SHA256)
                cipher = AES.new(layer_key, AES.MODE_GCM, nonce=nonce)
                
                try:
                    decrypted_chunk = cipher.decrypt_and_verify(ciphertext, tag)
                    outfile.write(decrypted_chunk)
                    total_chunks += 1
                except ValueError:
                    return {"status": "ERROR", "message": f"Decryption failed at scale {total_chunks}. Data corrupted or wrong password."}
                    
        secure_delete(encrypted_file_path)
                    
    except Exception as e:
        print(f"[SCALES] Decryption error: {e}")
        return {"status": "ERROR", "message": str(e)}

    return {
        "file": output_path,
        "status": "UNROLLED",
        "message": "Decryption successful."
    }
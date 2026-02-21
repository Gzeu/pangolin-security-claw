import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

CHUNK_SIZE = 1024 * 64  

def encrypt_file_scales(file_path: str):
    if not os.path.exists(file_path):
        return {"status": "ERROR", "message": "File not found."}

    print(f"[SCALES] Applying armored scales to: {file_path}")
    
    output_path = f"{file_path}.pangolin"
    
    # [*** VULNERABILITY: HARDCODED/RANDOM MASTER KEY WITHOUT PERSISTENCE ***]
    # In a real app, `master_key` MUST be derived from a user password using a KDF (like PBKDF2 or Argon2).
    # Currently, a random key is generated every time. 
    master_key = get_random_bytes(32) 
    
    total_chunks = 0
    encrypted_scales_meta = []

    try:
        with open(file_path, "rb") as infile, open(output_path, "wb") as outfile:
            outfile.write(b"PANGOLIN_V1")
            
            # [*** VULNERABILITY: KEY STORED IN PLAINTEXT ***]
            # The master key is written directly into the file header so the current decryption logic works.
            # This completely defeats the purpose of encryption, as anyone with the file has the key.
            # Fix: Remove this line. The user must provide the password/key during decryption.
            outfile.write(master_key)
            
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                # [*** WEAKNESS: WEAK KDF FOR CHUNKS ***]
                # Using simple SHA256(master_key + index) is fast but a bit naive.
                # A proper HKDF (HMAC-based Extract-and-Expand Key Derivation Function) is recommended.
                layer_key = hashlib.sha256(master_key + str(total_chunks).encode()).digest()
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
                
        # [*** WEAKNESS: SECURE DELETE MISSING ***]
        # os.remove(file_path) is commented out. Even if active, os.remove() does not securely wipe the disk.
        # An attacker can recover the original plaintext file using forensic tools.
                
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

def decrypt_file_scales(encrypted_file_path: str):
    if not os.path.exists(encrypted_file_path) or not encrypted_file_path.endswith(".pangolin"):
        return {"status": "ERROR", "message": "Invalid or missing .pangolin file."}

    print(f"[SCALES] Unrolling scales for: {encrypted_file_path}")
    output_path = encrypted_file_path[:-9]
    
    try:
        with open(encrypted_file_path, "rb") as infile, open(output_path, "wb") as outfile:
            header = infile.read(11)
            if header != b"PANGOLIN_V1":
                 return {"status": "ERROR", "message": "Invalid file format."}
                 
            # [*** VULNERABILITY: READING PLAINTEXT KEY ***]
            # This relies on the key being stored inside the file.
            master_key = infile.read(32)
            total_chunks = 0
            
            # [*** WEAKNESS: NO FILE INTEGRITY CHECK ***]
            # AES-GCM checks chunk integrity, but there is no global signature for the entire file.
            # An attacker could drop chunks, reorder chunks, or append garbage at the end.
            
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
                
                # [*** VULNERABILITY: MEMORY EXHAUSTION (DOS) ***]
                # If an attacker maliciously modifies `ct_len` to be 2GB, `infile.read(2GB)` 
                # will attempt to allocate 2GB of RAM, crashing the Python process.
                ciphertext = infile.read(ct_len)
                
                layer_key = hashlib.sha256(master_key + str(total_chunks).encode()).digest()
                cipher = AES.new(layer_key, AES.MODE_GCM, nonce=nonce)
                
                try:
                    decrypted_chunk = cipher.decrypt_and_verify(ciphertext, tag)
                    outfile.write(decrypted_chunk)
                    total_chunks += 1
                except ValueError:
                    return {"status": "ERROR", "message": f"Decryption failed at scale {total_chunks}. Data corrupted."}
                    
    except Exception as e:
        print(f"[SCALES] Decryption error: {e}")
        return {"status": "ERROR", "message": str(e)}

    return {
        "file": output_path,
        "status": "UNROLLED",
        "message": "Decryption successful."
    }
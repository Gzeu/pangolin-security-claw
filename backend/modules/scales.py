import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

CHUNK_SIZE = 1024 * 64  # 64KB per scale layer

def encrypt_file_scales(file_path: str):
    """
    Encrypts a file by chunking it into 'scales' using AES-256 GCM.
    Writes the encrypted output to a new file with a .pangolin extension.
    Returns metadata about the encryption process.
    """
    if not os.path.exists(file_path):
        return {"status": "ERROR", "message": "File not found."}

    print(f"[SCALES] Applying armored scales to: {file_path}")
    
    output_path = f"{file_path}.pangolin"
    master_key = get_random_bytes(32) # In a real app, this should be derived from a user password via PBKDF2
    
    total_chunks = 0
    encrypted_scales_meta = []

    try:
        with open(file_path, "rb") as infile, open(output_path, "wb") as outfile:
            # We write a dummy header to identify .pangolin files
            outfile.write(b"PANGOLIN_V1")
            
            # Write the master key (INSECURE FOR PROD - just for demonstration so decryption works)
            # A real implementation would encrypt the master key with a user password.
            outfile.write(master_key)
            
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                # Derive a specific key for this layer/scale to ensure chunk independence
                layer_key = hashlib.sha256(master_key + str(total_chunks).encode()).digest()
                cipher = AES.new(layer_key, AES.MODE_GCM)
                
                ciphertext, tag = cipher.encrypt_and_digest(chunk)
                
                # Write metadata needed for decryption: nonce length (16), nonce, tag length (16), tag, ciphertext length, ciphertext
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
                
        # Optional: Remove original file after encryption for true security
        # os.remove(file_path)
                
    except Exception as e:
        print(f"[SCALES] Encryption error: {e}")
        return {"status": "ERROR", "message": str(e)}

    print(f"[SCALES] File armored successfully. Created {total_chunks} scales.")
    return {
        "file": output_path,
        "original_file": file_path,
        "total_scales": total_chunks,
        "scales_data": encrypted_scales_meta,
        "status": "ARMORED"
    }

def decrypt_file_scales(encrypted_file_path: str):
    """
    Decrypts a .pangolin file back to its original form.
    """
    if not os.path.exists(encrypted_file_path) or not encrypted_file_path.endswith(".pangolin"):
        return {"status": "ERROR", "message": "Invalid or missing .pangolin file."}

    print(f"[SCALES] Unrolling scales for: {encrypted_file_path}")
    
    # Strip the .pangolin extension for the output
    output_path = encrypted_file_path[:-9]
    
    try:
        with open(encrypted_file_path, "rb") as infile, open(output_path, "wb") as outfile:
            header = infile.read(11)
            if header != b"PANGOLIN_V1":
                 return {"status": "ERROR", "message": "Invalid file format."}
                 
            master_key = infile.read(32)
            total_chunks = 0
            
            while True:
                # Read Nonce
                nonce_len_bytes = infile.read(4)
                if not nonce_len_bytes:
                    break # EOF
                nonce_len = int.from_bytes(nonce_len_bytes, 'little')
                nonce = infile.read(nonce_len)
                
                # Read Tag
                tag_len_bytes = infile.read(4)
                tag_len = int.from_bytes(tag_len_bytes, 'little')
                tag = infile.read(tag_len)
                
                # Read Ciphertext
                ct_len_bytes = infile.read(4)
                ct_len = int.from_bytes(ct_len_bytes, 'little')
                ciphertext = infile.read(ct_len)
                
                # Decrypt
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

    print(f"[SCALES] File unrolled successfully. Restored {total_chunks} scales.")
    return {
        "file": output_path,
        "status": "UNROLLED",
        "message": "Decryption successful."
    }
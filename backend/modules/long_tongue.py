import os
import re

LEAK_PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GITHUB_TOKEN":   re.compile(r"gh[pousr]_[A-Za-z0-9_]{36}"),
    "STRIPE_KEY":     re.compile(r"(sk_live|sk_test)_[0-9a-zA-Z]{24}"),
    "GENERIC_SECRET": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password)[\s:=]+[\"']?([a-zA-Z0-9\-_]{20,})[\"']?"
    ),
}

IGNORE_DIRS = {".git", "node_modules", "venv", "__pycache__", "build", "dist", ".venv"}
SCANNABLE_EXTENSIONS = {".env", ".json", ".log", ".yaml", ".yml", ".txt", ".py", ".js"}

def search_leaks(target_directory: str = "."):
    print(f"[LONG TONGUE] Scanning directory: {target_directory}")
    results = []
    seen = set()

    for root, dirs, files in os.walk(target_directory):
        # [*** WEAKNESS: SYMLINK LOOPING ***]
        # `os.walk` defaults to `followlinks=False`, which is good, but if a user explicitly 
        # configures it to follow links, an attacker could create an infinite symlink loop.
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in SCANNABLE_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)
            
            # [*** VULNERABILITY: LARGE FILE DoS (BOMB) ***]
            # `os.path.getsize(file_path)` is not checked.
            # If an attacker places a 50GB `.log` file in the directory, `f.read()` will attempt 
            # to load 50GB into RAM, crashing the system.
            # Fix: Read in chunks or skip files larger than a specific limit (e.g., 5MB).

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for leak_type, pattern in LEAK_PATTERNS.items():
                    # [*** WEAKNESS: RE-DoS (Regular Expression Denial of Service) ***]
                    # While these specific patterns are relatively safe, complex regexes can be 
                    # exploited with crafted strings that cause catastrophic backtracking, freezing the thread.
                    if pattern.search(content):
                        confidence = 0.99 if leak_type != "GENERIC_SECRET" else 0.82
                        key = (file_path, leak_type)
                        if key not in seen:
                            seen.add(key)
                            results.append({
                                "file": file_path,
                                "leak_type": leak_type,
                                "confidence_score": confidence
                            })
            except PermissionError:
                print(f"[LONG TONGUE] Permission denied: {file_path}")
            except Exception as e:
                print(f"[LONG TONGUE] Error reading {file_path}: {e}")

    print(f"[LONG TONGUE] Done. Found {len(results)} potential leaks.")
    return results
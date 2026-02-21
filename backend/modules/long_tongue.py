import os
import re

# Regex patterns for common credential leaks
# Strictly typed, no external ML libraries required.
LEAK_PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GITHUB_TOKEN":   re.compile(r"gh[pousr]_[A-Za-z0-9_]{36}"),
    "STRIPE_KEY":     re.compile(r"(sk_live|sk_test)_[0-9a-zA-Z]{24}"),
    "GENERIC_SECRET": re.compile(
        r"(?i)(?:api[_-]?key|secret|token|password)[\s:=]+[\"']?([a-zA-Z0-9\-_]{20,})[\"']?"
    ),
}

# Directories to skip entirely to avoid performance or permission issues
IGNORE_DIRS = {".git", "node_modules", "venv", "__pycache__", "build", "dist", ".venv"}

# File extensions to scan
SCANNABLE_EXTENSIONS = {".env", ".json", ".log", ".yaml", ".yml", ".txt", ".py", ".js"}

def search_leaks(target_directory: str = "."):
    """
    Scans local files for exposed credentials using regex patterns.
    Pure stdlib: os + re. Zero external dependencies.
    """
    print(f"[LONG TONGUE] Scanning directory: {target_directory}")
    results = []
    seen = set()

    for root, dirs, files in os.walk(target_directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in SCANNABLE_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for leak_type, pattern in LEAK_PATTERNS.items():
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

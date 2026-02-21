import os
import re

# Regex patterns for common secrets
LEAK_PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GITHUB_TOKEN": re.compile(r"gh[p|o|u|s|r]_[A-Za-z0-9_]{36}"),
    "GENERIC_API_KEY": re.compile(r"(?i)(api[_-]?key|secret|token|password)[\s:=]+[\"']?([a-zA-Z0-9\-_]{16,})[\"']?"),
    "STRIPE_KEY": re.compile(r"(sk_live|sk_test)_[0-9a-zA-Z]{24}")
}

# Directories to ignore during the scan to prevent performance issues
IGNORE_DIRS = {".git", "node_modules", "venv", "__pycache__", "build", "dist"}

def search_leaks(target_directory: str = "."):
    """
    Scans files in the target directory for exposed secrets using regex patterns.
    Functions as the 'Long Tongue' seeking out vulnerabilities.
    """
    print(f"[LONG TONGUE] Deep searching for leaks in directory: {target_directory}")
    results = []

    for root, dirs, files in os.walk(target_directory):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            # We focus on files that commonly contain configurations or logs
            if not file.endswith((".env", ".json", ".log", ".yaml", ".yml", ".txt", ".js", ".py")):
                continue

            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                    for leak_type, pattern in LEAK_PATTERNS.items():
                        matches = pattern.finditer(content)
                        for match in matches:
                            # We assign a high confidence score since it's a direct regex match
                            # AWS and GitHub tokens are very precise, generic ones are slightly less so.
                            confidence = 0.99 if leak_type != "GENERIC_API_KEY" else 0.85
                            
                            # Avoid adding exact duplicate matches from the same file
                            leak_entry = {
                                "file": file_path,
                                "leak_type": leak_type,
                                "confidence_score": confidence
                            }
                            
                            if leak_entry not in results:
                                results.append(leak_entry)
            except Exception as e:
                print(f"[ERROR] Long Tongue could not read {file_path}: {e}")

    print(f"[LONG TONGUE] Search complete. Found {len(results)} potential leaks.")
    return results
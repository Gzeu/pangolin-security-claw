import random

def search_leaks(query: str):
    """
    Simulates an embedding search through .log, .json, and .env files to find data leaks.
    """
    print(f"[LONG TONGUE] Deep searching for leaks related to: {query}")
    
    mock_files = ["config/.env", "logs/auth.log", "data/users.json"]
    leak_types = ["API_KEY", "PASSWORD", "AWS_TOKEN"]
    
    results = []
    for f in mock_files:
        confidence = random.uniform(0.65, 0.99)
        if confidence > 0.8:
            results.append({
                "file": f,
                "leak_type": random.choice(leak_types),
                "confidence_score": round(confidence, 2)
            })
            
    return results
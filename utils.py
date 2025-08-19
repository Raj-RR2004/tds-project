import json

def safe_json_dumps(data):
    """Safely convert Python objects to JSON string."""
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Serialization failed: {str(e)}"})

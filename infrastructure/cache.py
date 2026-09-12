from domain.types import AnalysisResult

def get_cached_result(redis_client, text):
    try:
        key = text_hash(text)
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None
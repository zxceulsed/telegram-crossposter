import hashlib

def generate_sig(params: dict, session_secret_key: str) -> str:
    sorted_items = "".join(f"{k}={params[k]}" for k in sorted(params))
    raw = f"{sorted_items}{session_secret_key}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()

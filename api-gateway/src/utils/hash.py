import hashlib


def string_to_md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

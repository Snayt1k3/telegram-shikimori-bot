import hashlib


def convert_to_md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

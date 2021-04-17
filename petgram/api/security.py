import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(bytearray(password, "utf8")).hexdigest()


def is_same_password(password1: str, password2: str) -> bool:
    return hash_password(password1).upper() == password2.upper()
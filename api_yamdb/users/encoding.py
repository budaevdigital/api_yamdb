import base64
from hashlib import blake2b
from hmac import compare_digest
from random import choice

SALT_PHRASE_KEY = b'2B402A375F706178732B356279786C29375E2A7571396E392D3277'
AUTH_SIZE = 16


def encode_code(code: str) -> bytes:
    phrase = base64.b16encode(code.encode())
    hash = blake2b(digest_size=AUTH_SIZE, key=SALT_PHRASE_KEY)
    hash.update(phrase)
    return hash.hexdigest().encode('utf-8')


def verify_code(code: str, hash: bytes) -> bool:
    good_sig = encode_code(code)
    return compare_digest(good_sig, hash)


def generate_code() -> str:
    """
    Генерирует код из 6 символов
    """
    seeds = '1234567890abcdefghijklmnopqrstuvwxyz'
    random_str = []
    for i in range(6):
        random_str.append(choice(seeds))
    return ''.join(random_str).upper()

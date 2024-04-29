#p2pkh.py
import hashlib

from Utils import base58
from Utils.base58 import b58encode
from Utils.util import extract_pubkey_hash


def p2pkh(scriptpubkey_asm: str) -> bytes:
    pubkey_hash = extract_pubkey_hash(scriptpubkey_asm.split(" "))
    pubkey_hash_bytes = bytes.fromhex(pubkey_hash)
    version_byte = b"\x00"
    payload = version_byte + pubkey_hash_bytes
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum)
    return address

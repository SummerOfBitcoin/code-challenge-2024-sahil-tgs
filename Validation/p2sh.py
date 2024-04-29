#p2sh.py
import hashlib
from Utils import base58
from Utils.util import extract_pubkey_hash


def p2sh(scriptpubkey_asm: str) -> bytes:
    script_hash = extract_pubkey_hash(scriptpubkey_asm.split(" "))
    script_hash_bytes = bytes.fromhex(script_hash)
    version_byte = b"\x05"
    payload = version_byte + script_hash_bytes
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum)
    return address

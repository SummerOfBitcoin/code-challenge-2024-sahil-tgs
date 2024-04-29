#utils.py
import hashlib

from Structs.struct import Transaction


def extract_pubkey_hash(script_pubkey_asm: str) -> str:
    parts = script_pubkey_asm.split(' ')
    for i in range(len(parts)):
        if parts[i] in ['OP_PUSHBYTES_20', 'OP_PUSHBYTES_32']:
            return parts[i + 1]
    return ''


def to_sha(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def read_json_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def handle_error(error: Exception):
    if error:
        print(error)


def check_segwit(tx: Transaction) -> bool:
    for vin in tx.vin:
        if len(vin.witness) > 0:
            return True
    return False


def reverse_bytes(data: bytes) -> bytes:
    return data[::-1]



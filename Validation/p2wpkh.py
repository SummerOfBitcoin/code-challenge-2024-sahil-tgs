# p2wpkh.py
from typing import List
from Utils.util import extract_pubkey_hash
from Utils.bech32 import encode

def p2wpkh(scriptpubkey_asm: str) -> bytes:
    witness_program = extract_pubkey_hash(scriptpubkey_asm.split(" "))
    witness_program_bytes = bytes.fromhex(witness_program)
    version = 0x00
    payload = [version] + convertbits(witness_program_bytes, 8, 5)
    address = encode("bc", payload)
    return address.encode()

def convertbits(data: bytes, frombits: int, tobits: int, pad: bool = True) -> List[int]:
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for d in data:
        acc = (acc << frombits) | d
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret
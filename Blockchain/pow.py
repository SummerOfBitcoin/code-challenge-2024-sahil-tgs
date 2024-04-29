#pow.py

import hashlib
from typing import List
from Structs.struct import BlockHeader
from Utils.util import reverse_bytes, to_sha
from Utils.serialize import serialize_block_header
target = "0000ffff00000000000000000000000000000000000000000000000000000000"

def compare_byte_arrays(a: bytes, b: bytes) -> int:
    if len(a) != len(b):
        raise ValueError("Arrays must have the same length")
    for i in range(len(a)):
        if a[i] < b[i]:
            return -1
        elif a[i] > b[i]:
            return 1
    return 0

def proof_of_work(bh: BlockHeader) -> bool:
    target_bytes = bytes.fromhex(target)
    while True:
        serialized = serialize_block_header(bh)
        hash_val = reverse_bytes(to_sha(to_sha(serialized)))
        if compare_byte_arrays(hash_val, target_bytes) == -1:
            print(f"Block Mined: {hash_val.hex()}")
            return True
        if bh.nonce < 0x0 or bh.nonce > 0xffffffff:
            print("FUCKED")
            return False
        bh.nonce += 1
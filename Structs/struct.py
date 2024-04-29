#struct.py

from typing import List


class BlockHeader:
    def __init__(self, version: int, prev_block_hash: str, merkle_root: str, timestamp: int, bits: int, nonce: int):
        self.version = version
        self.prev_block_hash = prev_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce


class Input:
    def __init__(self, txid: str, vout: int, prevout: dict, scriptsig: str, scriptsig_asm: str, witness: List[str],
                 is_coinbase: bool, sequence: int):
        self.txid = txid
        self.vout = vout
        self.prevout = Prevout(**prevout)
        self.scriptsig = scriptsig
        self.scriptsig_asm = scriptsig_asm
        self.witness = witness
        self.is_coinbase = is_coinbase
        self.sequence = sequence


class Prevout:
    def __init__(self, scriptpubkey: str, scriptpubkey_asm: str, scriptpubkey_type: str, scriptpubkey_address: str,
                 value: int):
        self.scriptpubkey = scriptpubkey
        self.scriptpubkey_asm = scriptpubkey_asm
        self.scriptpubkey_type = scriptpubkey_type
        self.scriptpubkey_address = scriptpubkey_address
        self.value = value


class Transaction:
    def __init__(self, version: int, locktime: int, vin: List[dict], vout: List[dict], scriptpubkey: str = ''):
        self.version = version
        self.locktime = locktime
        self.vin = [Input(**input_data) for input_data in vin]
        self.vout = [Prevout(**output_data) for output_data in vout]
        self.scriptpubkey = scriptpubkey


class TxInfo:
    def __init__(self, txid: str, wtxid: str, fee: int, weight: int):
        self.txid = txid
        self.wtxid = wtxid
        self.fee = fee
        self.weight = weight


class TxWeight:
    def __init__(self, base_size: int, witness_size: int, weight: int):
        self.base_size = base_size
        self.witness_size = witness_size
        self.weight = weight


class MerkleNode:
    def __init__(self, left: 'MerkleNode' = None, right: 'MerkleNode' = None, data: bytes = None):
        self.left = left
        self.right = right
        self.data = data


class MerkleTree:
    def __init__(self, root: MerkleNode):
        self.root = root

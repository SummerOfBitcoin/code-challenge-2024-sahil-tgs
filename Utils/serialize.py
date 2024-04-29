#serialize.py
import struct
import time
from Structs.struct import Transaction, BlockHeader
from Utils import util


def uint16_to_bytes(n: int) -> bytes:
    return struct.pack("<H", n)


def uint32_to_bytes(n: int) -> bytes:
    return struct.pack("<I", n)


def uint64_to_bytes(n: int) -> bytes:
    return struct.pack("<Q", n)


def serialize_varint(n: int) -> bytes:
    if n < 0xfd:
        return bytes([n])
    elif n <= 0xffff:
        return b"\xfd" + uint16_to_bytes(n)
    elif n <= 0xffffffff:
        return b"\xfe" + uint32_to_bytes(n)
    else:
        return b"\xff" + uint64_to_bytes(n)


def serialize_transaction(tx: Transaction) -> tuple[bytes, None]:
    serialized = bytearray()

    # Serialize version
    version_bytes = uint32_to_bytes(tx.version)
    serialized.extend(version_bytes)

    # Serialize vin count
    vin_count = len(tx.vin)
    serialized.extend(serialize_varint(vin_count))

    # Serialize vin
    for vin in tx.vin:
        txid_bytes = bytes.fromhex(vin.txid)[::-1]
        serialized.extend(txid_bytes)

        vout_bytes = uint32_to_bytes(vin.vout)
        serialized.extend(vout_bytes)

        scriptsig_bytes = bytes.fromhex(vin.scriptsig)
        length_scriptsig = len(scriptsig_bytes)
        serialized.extend(serialize_varint(length_scriptsig))
        serialized.extend(scriptsig_bytes)

        sequence_bytes = uint32_to_bytes(vin.sequence)
        serialized.extend(sequence_bytes)

    # Serialize vout count
    vout_count = len(tx.vout)
    serialized.extend(serialize_varint(vout_count))

    # Serialize vout
    for vout in tx.vout:
        value_bytes = uint64_to_bytes(vout.value)
        serialized.extend(value_bytes)

        scriptpubkey_bytes = bytes.fromhex(vout.scriptpubkey)
        scriptpubkey_len = len(scriptpubkey_bytes)
        serialized.extend(serialize_varint(scriptpubkey_len))
        serialized.extend(scriptpubkey_bytes)

    # Serialize locktime
    locktime_bytes = uint32_to_bytes(tx.locktime)
    serialized.extend(locktime_bytes)

    return bytes(serialized), None


def segwit_serialize(tx: Transaction) -> tuple[bytes, None]:
    serialized = bytearray()
    is_segwit = util.check_segwit(tx)

    # Serialize version
    version_bytes = uint32_to_bytes(tx.version)
    serialized.extend(version_bytes)

    # Serialize vin count
    if is_segwit:
        serialized.extend(b"\x00\x01")

    vin_count = len(tx.vin)
    serialized.extend(serialize_varint(vin_count))

    # Serialize vin
    for vin in tx.vin:
        txid_bytes = bytes.fromhex(vin.txid)[::-1]
        serialized.extend(txid_bytes)

        vout_bytes = uint32_to_bytes(vin.vout)
        serialized.extend(vout_bytes)

        scriptsig_bytes = bytes.fromhex(vin.scriptsig)
        length_scriptsig = len(scriptsig_bytes)
        serialized.extend(serialize_varint(length_scriptsig))
        serialized.extend(scriptsig_bytes)

        sequence_bytes = uint32_to_bytes(vin.sequence)
        serialized.extend(sequence_bytes)

    # Serialize vout count
    vout_count = len(tx.vout)
    serialized.extend(serialize_varint(vout_count))

    # Serialize vout
    for vout in tx.vout:
        value_bytes = uint64_to_bytes(vout.value)
        serialized.extend(value_bytes)

        scriptpubkey_bytes = bytes.fromhex(vout.scriptpubkey)
        scriptpubkey_len = len(scriptpubkey_bytes)
        serialized.extend(serialize_varint(scriptpubkey_len))
        serialized.extend(scriptpubkey_bytes)

    # Serialize witness data
    if is_segwit:
        for vin in tx.vin:
            witness_count = len(vin.witness)
            serialized.extend(serialize_varint(witness_count))
            for witness in vin.witness:
                witness_bytes = bytes.fromhex(witness)
                witness_len = len(witness_bytes)
                serialized.extend(serialize_varint(witness_len))
                serialized.extend(witness_bytes)

    # Serialize locktime
    locktime_bytes = uint32_to_bytes(tx.locktime)
    serialized.extend(locktime_bytes)

    return bytes(serialized), None


def serialize_block_header(bh: BlockHeader) -> bytes:
    serialized = bytearray()

    version_bytes = uint32_to_bytes(bh.version)
    serialized.extend(version_bytes)

    prev_block_hash_bytes = bytes.fromhex(bh.prev_block_hash)[::-1]
    serialized.extend(prev_block_hash_bytes)

    merkle_root_bytes = bytes.fromhex(bh.merkle_root)[::-1]
    serialized.extend(merkle_root_bytes)

    bh.timestamp = int(time.time())
    time_bytes = uint32_to_bytes(bh.timestamp)
    serialized.extend(time_bytes)

    bits_bytes = uint32_to_bytes(bh.bits)
    serialized.extend(bits_bytes)

    nonce_bytes = uint32_to_bytes(bh.nonce)
    serialized.extend(nonce_bytes)

    return bytes(serialized)
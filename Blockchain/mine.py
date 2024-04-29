# mine.py
import time
from Structs.struct import BlockHeader
from Utils.prioritize import prioritize
from Utils.coinbase import create_coinbase
from Utils.serialize import serialize_transaction, serialize_block_header, segwit_serialize
from Utils.merkle import new_merkle_tree
from Utils.util import to_sha, reverse_bytes
from Blockchain.pow import proof_of_work
from Utils.weight import calculate_base_size, calculate_witness_size

bh = BlockHeader(
    version=7,
    prev_block_hash="0000000000000000000000000000000000000000000000000000000000000000",
    merkle_root="",
    timestamp=int(time.time()),
    bits=0x1f00ffff,
    nonce=0,
)


def mine_block():
    net_reward, tx_ids, _ = prioritize()
    cb_tx = create_coinbase(net_reward)
    serialized_cb_tx = serialize_transaction(cb_tx)
    print(f"CBTX: {serialized_cb_tx.hex()}")
    tx_ids.insert(0, reverse_bytes(to_sha(to_sha(serialized_cb_tx))).hex())
    mkr = new_merkle_tree(tx_ids)
    bh.merkle_root = mkr.data.hex()
    from Utils.weight import calculate_base_size
    cbtx_base = calculate_base_size(cb_tx)
    from Utils.weight import calculate_witness_size
    cbtx_witness = calculate_witness_size(cb_tx)
    print(f"Cbtx wt: {cbtx_witness + (cbtx_base * 4)}")
    if proof_of_work(bh):
        with open("output.txt", "w") as file:
            serialized_bh = serialize_block_header(bh)
            seg_serialized = segwit_serialize(cb_tx)
            file.write(serialized_bh.hex() + "\n")
            file.write(seg_serialized.hex() + "\n")
            for tx in tx_ids:
                file.write(tx + "\n")

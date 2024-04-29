#prioritize.py

import os
import json
from typing import List, Tuple
from Structs.struct import Transaction, TxInfo
from Utils.serialize import serialize_transaction, segwit_serialize
from Utils.util import to_sha, reverse_bytes, read_json_file
from Utils.weight import calculate_witness_size, calculate_base_size


def comp(a: TxInfo, b: TxInfo) -> bool:
    return a.fee / a.weight > b.fee / b.weight


def prioritize() -> Tuple[int, List[str], List[str]]:
    permitted_txids = []
    permitted_wtxids = []
    mempool_dir = "./mempool"
    files = os.listdir(mempool_dir)
    tx_info_list = []
    for file in files:
        tx_data = read_json_file(os.path.join(mempool_dir, file))
        tx = json.loads(tx_data, object_hook=lambda d: Transaction(**d))
        fee = sum(vin.prevout.value for vin in tx.vin) - sum(vout.value for vout in tx.vout)
        serialized = serialize_transaction(tx)
        seg_serialized = segwit_serialize(tx)
        txid = reverse_bytes(to_sha(to_sha(serialized))).hex()
        wtxid = reverse_bytes(to_sha(to_sha(seg_serialized))).hex()
        tx_info = TxInfo(txid=txid, wtxid=wtxid, fee=fee,
                         weight=calculate_witness_size(tx) + calculate_base_size(tx) * 4)
        tx_info_list.append(tx_info)
    tx_info_list.sort(key=lambda tx_info: comp(tx_info, TxInfo(txid="", wtxid="", fee=0, weight=0)), reverse=True)
    permissible_txs = []
    permissible_weight = 3999300
    reward = 0
    for tx_info in tx_info_list:
        if permissible_weight >= tx_info.weight:
            permissible_txs.append(tx_info)
            permissible_weight -= tx_info.weight
            permitted_txids.append(tx_info.txid)
            permitted_wtxids.append(tx_info.wtxid)
            reward += tx_info.fee
    print("weight: ", permissible_weight)
    print("reward: ", reward)
    return reward, permitted_txids, permitted_wtxids

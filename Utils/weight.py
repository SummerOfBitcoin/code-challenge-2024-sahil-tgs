#weight.py
from Structs.struct import Transaction
from Utils.serialize import serialize_transaction, segwit_serialize
from Utils.util import check_segwit


def calculate_base_size(tx: Transaction) -> int:
    serialized = serialize_transaction(tx)
    return len(serialized)


def calculate_witness_size(tx: Transaction) -> int:
    if not check_segwit(tx):
        return 0
    serialized = segwit_serialize(tx)
    return len(serialized)

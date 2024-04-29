#coinbase.py
from Structs.struct import Transaction, Input, Prevout
from Utils.merkle import create_witness_merkle


def create_coinbase(net_reward: int) -> Transaction:
    witness_commitment = create_witness_merkle()
    coinbase_tx = Transaction(
        version=1,
        vin=[
            Input(
                txid="0000000000000000000000000000000000000000000000000000000000000000",
                vout=0xffffffff,
                prevout=Prevout(
                    scriptpubkey="0014df4bf9f3621073202be59ae590f55f42879a21a0",
                    scriptpubkey_asm="0014df4bf9f3621073202be59ae590f55f42879a21a0",
                    scriptpubkey_type="p2pkh",
                    scriptpubkey_address="bc1qma9lnumzzpejq2l9ntjepa2lg2re5gdqn3nf0c",
                    value=net_reward,
                ),
                is_coinbase=True,
                sequence=0xffffffff,
                scriptsig="03951a0604f15ccf5609013803062b9b5a0100072f425443432f20",
                witness=["0000000000000000000000000000000000000000000000000000000000000000"],
            )
        ],
        vout=[
            Prevout(
                scriptpubkey="0014df4bf9f3621073202be59ae590f55f42879a21a0",
                scriptpubkey_asm="0014df4bf9f3621073202be59ae590f55f42879a21a0",
                scriptpubkey_type="p2pkh",
                scriptpubkey_address="bc1qma9lnumzzpejq2l9ntjepa2lg2re5gdqn3nf0c",
                value=net_reward,
            ),
            Prevout(
                scriptpubkey="6a24aa21a9ed" + witness_commitment,
                scriptpubkey_asm="OP_RETURNOP_PUSHBYTES_36aa21a9ed" + witness_commitment,
                scriptpubkey_type="op_return",
                scriptpubkey_address="bc1qma9lnumzzpejq2l9ntjepa2lg2re5gdqn3nf0c",
                value=0,
            ),
        ],
        locktime=0,
    )
    return coinbase_tx

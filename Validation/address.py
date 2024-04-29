#address.py
import os
import json
from typing import List
from Structs.struct import Transaction
from Validation.p2pkh import p2pkh
from Validation.p2sh import p2sh
from Validation.p2wpkh import p2wpkh
from Validation.p2wsh import p2wsh
from Utils.util import handle_error, read_json_file

ct_p2pkh = 0
ct_p2sh = 0
ct_p2wpkh = 0
ct_p2wsh = 0


def validate_address():
    global ct_p2pkh, ct_p2sh, ct_p2wpkh, ct_p2wsh
    mempool_dir = "./mempool"
    files = os.listdir(mempool_dir)
    for file in files:
        tx_data = read_json_file(os.path.join(mempool_dir, file))
        tx = Transaction(**json.loads(tx_data))
        for vin in tx.vin:
            if vin.prevout.scriptpubkey_type == "p2pkh":
                pubkey_asm = vin.prevout.scriptpubkey_asm
                address = p2pkh(pubkey_asm)
                if address.decode() == vin.prevout.scriptpubkey_address:
                    ct_p2pkh += 1
                    continue
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vin.prevout.scriptpubkey_address)

            if vin.prevout.scriptpubkey_type == "p2sh":
                pubkey_asm = vin.prevout.scriptpubkey_asm
                address = p2sh(pubkey_asm)
                if address.decode() == vin.prevout.scriptpubkey_address:
                    ct_p2sh += 1
                    continue
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vin.prevout.scriptpubkey_address)

            if vin.prevout.scriptpubkey_type == "v0_p2wpkh":
                pubkey_asm = vin.prevout.scriptpubkey_asm
                address = p2wpkh(pubkey_asm)
                if address.decode() == vin.prevout.scriptpubkey_address:
                    ct_p2wpkh += 1
                    continue
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vin.prevout.scriptpubkey_address)

            if vin.prevout.scriptpubkey_type == "v0_p2wsh":
                pubkey_asm = vin.prevout.scriptpubkey_asm
                address = p2wsh(pubkey_asm)
                if address.decode() == vin.prevout.scriptpubkey_address:
                    ct_p2wsh += 1
                    continue
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vin.prevout.scriptpubkey_address)

        for vout in tx.vout:
            if vout.scriptpubkey_type == "p2pkh":
                pubkey_asm = vout.scriptpubkey_asm
                address = p2pkh(pubkey_asm)
                if address.decode() == vout.scriptpubkey_address:
                    ct_p2pkh += 1
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vout.scriptpubkey_address)

            if vout.scriptpubkey_type == "p2sh":
                pubkey_asm = vout.scriptpubkey_asm
                address = p2sh(pubkey_asm)
                if address.decode() == vout.scriptpubkey_address:
                    ct_p2sh += 1
                    continue
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vout.scriptpubkey_address)

            if vout.scriptpubkey_type == "v0_p2wpkh":
                pubkey_asm = vout.scriptpubkey_asm
                address = p2wpkh(pubkey_asm)
                if address.decode() == vout.scriptpubkey_address:
                    ct_p2wpkh += 1
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vout.scriptpubkey_address)

            if vout.scriptpubkey_type == "v0_p2wsh":
                pubkey_asm = vout.scriptpubkey_asm
                address = p2wsh(pubkey_asm)
                if address.decode() == vout.scriptpubkey_address:
                    ct_p2wsh += 1
                else:
                    print("Address not matched")
                    print("Address: ", address.decode())
                    print("Scriptpubkey Address: ", vout.scriptpubkey_address)

    print("Count of p2pkh address matched: ", ct_p2pkh)
    print("Count of p2sh address matched: ", ct_p2sh)
    print("Count of p2wpkh address matched: ", ct_p2wpkh)
    print("Count of p2wsh address matched: ", ct_p2wsh)
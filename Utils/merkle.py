#merkle.py

from typing import List
from Structs.struct import MerkleNode
from Utils.prioritize import prioritize
from Utils.util import to_sha, reverse_bytes


def new_merkle_node(lnode: MerkleNode = None, rnode: MerkleNode = None, data: bytes = None) -> MerkleNode:
    mNode = MerkleNode()
    if lnode is None and rnode is None:
        mNode.data = reverse_bytes(data)
    else:
        prevHash = lnode.data + rnode.data
        mNode.data = to_sha(to_sha(prevHash))
    mNode.left = lnode
    mNode.right = rnode
    return mNode


def new_merkle_tree(leaves: List[str]) -> MerkleNode:
    nodes = [new_merkle_node(data=bytes.fromhex(leaf)) for leaf in leaves]
    while len(nodes) > 1:
        new_level = []
        for i in range(0, len(nodes), 2):
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])
            new_level.append(new_merkle_node(nodes[i], nodes[i + 1]))
        nodes = new_level
    return nodes[0]


def create_witness_merkle() -> str:
    _, _, wtxids = prioritize()
    wtxids.insert(0, "0000000000000000000000000000000000000000000000000000000000000000")
    merkle_root = new_merkle_tree(wtxids)
    print("WMKR: ", merkle_root.data.hex())
    commitment_string = merkle_root.data.hex() + "0000000000000000000000000000000000000000000000000000000000000000"
    witness_commitment = bytes.fromhex(commitment_string)
    witness_commitment = to_sha(to_sha(witness_commitment))
    print("Witness Commitment: ", witness_commitment.hex())
    return witness_commitment.hex()

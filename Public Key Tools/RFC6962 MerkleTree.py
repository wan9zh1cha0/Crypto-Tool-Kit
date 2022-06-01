'''
RFC 6962 Merkle Tree Hash implementation
'''

from hashlib import sha256
import time

def find_k(n):
    """
    input: an integer n
    output: largest power of two < n
    """
    i = 1
    while 2 ** i < n:
        i += 1
    i -= 1
    return 2 ** i

def cal_sha(x):
    """
    input: x (a string of any length)
    output: sha256(x) (Hexadecimal string of length 64)
    """
    return sha256(x).digest()

def MerkleTree_hash(data):
    """
    input: data (a list of strings)
    output: root of the merkle tree
    """
    n = len(data)
    if n == 0:
        return cal_sha(b'')
    elif n == 1:
        return cal_sha(b'\x00' + data[0])
    else:
        k = find_k(n)
        return cal_sha(b'\x01' + MerkleTree_hash(data[:k]) + MerkleTree_hash(data[k:]))


def auditPath(m, data):
    """
    obtain the audit path of a block
    input: the index of the block to be verified (m), the input data list
    output: the audit path for the block
    """
    n = len(data)
    if m >= n or m < 0:
        print('Input ERROR!')
        return False
    if n == 1:
        return []
    k = find_k(n)
    if m < k:
        return auditPath(m, data[:k]) + [[MerkleTree_hash(data[k:]), 0]]
    else:
        return auditPath(m - k, data[k:]) + [[MerkleTree_hash(data[:k]), 1]]
  

def audit(leaf, path, root):
    """
    verify the leaf node with the audit path
    input: leaf node value, audit path, root hash value
    output: True or False
    """
    vrfy = cal_sha(b'\x00' + leaf)
    for block in path:
        h = block[0]
        tag = block[1]
        if tag == 0:
            vrfy = cal_sha(b'\x01' + vrfy + h)
        else:
            vrfy = cal_sha(b'\x01' + h + vrfy)
    if vrfy == root:
        return True
    else:
        return False
    
if __name__ == '__main__':
    # data = [str(i) for i in range(100000)]
    data = [str(i).encode() for i in range(0, 100000)]
    t1 = time.perf_counter()
    mt = MerkleTree_hash(data)
    t2 = time.perf_counter()
    print(t2-t1)
    print('MTH of 100k leaf nodes:')
    print(mt.hex())
    data = [str(i).encode() for i in range(100000)]
    ap = auditPath(201, data)
    print('audit path:')
    print([[x[0].hex(), x[1]] for x in ap])
    print(audit(data[201], ap, mt))
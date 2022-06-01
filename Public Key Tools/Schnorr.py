import tools as t
import elliptic_curve as ec
from random import randint

def KeyGen(curve):
    sk = randint(0, curve.n - 1)
    pk = ec.calculate_dG(sk, curve.G, curve)
    return (sk, pk)

def Sign(M, sk, curve):
    n = curve.n
    G = curve.G
    k = randint(0, n - 1)
    R = ec.calculate_dG(k, G, curve)
    e = t.cal_sha1(bytes(str(R[0]) + str(R[1]) + str(M, 'utf-8'), 'utf-8'))
    s = (k + t.fast_mul(e, sk, n)) % n
    return (R, s)

def Verify(M, sig, pk, curve):
    G = curve.G
    R, s = sig
    e = t.cal_sha1(bytes(str(R[0]) + str(R[1]) + str(M, 'utf-8'), 'utf-8'))
    sG = ec.calculate_dG(s, G, curve)
    R_eP = ec.add_P_Q(R, ec.calculate_dG(e, pk, curve), curve)
    print(sG, R_eP)
    if sG == R_eP:
        return True
    else:
        return False
    
if __name__ == "__main__":
    sk, pk = KeyGen(ec.curve)
    M = b'test of Schnorr!!!'
    sig = Sign(M, sk, ec.curve)
    if Verify(M, sig, pk, ec.curve):
        print("verification passed.")
    else:
        print("verification failed.")
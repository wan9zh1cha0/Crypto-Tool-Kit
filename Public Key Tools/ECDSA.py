import tools as t
import elliptic_curve as ec
from random import randint

def KeyGen(curve):
    sk = randint(0, curve.n - 1)
    pk = ec.calculate_dG(sk, curve.G, curve)
    return (sk, pk)

def Sign(m, sk, curve):
    G = curve.G
    n = curve.n
    r = 0
    s = 0
    while r == 0 or s == 0:
        k = randint(0, n - 1)
        R = ec.calculate_dG(k, G, curve)
        r = R[0] % n
        e = t.cal_sha1(m)
        s = t.fast_mul(t.inverse(k, n), e + t.fast_mul(sk, r, n), n)
    return (r, s)

def Verify(m, sig, pk, curve):
    G = curve.G
    n = curve.n
    (r, s) = sig
    e = t.cal_sha1(m)
    w = t.inverse(s, n)
    m1 = t.fast_mul(e, w, n)
    m2 = t.fast_mul(r, w, n)
    t1 = ec.calculate_dG(m1, G, curve)
    t2 = ec.calculate_dG(m2, pk, curve)
    (r_, s_) = ec.add_P_Q(t1, t2, curve)
    if r == r_:
        return True, (r_, s_)
    else:
        return False, (r_, s_)

if __name__ == "__main__":
    sk, pk = KeyGen(ec.curve)
    print("secret key:\t", sk)
    print("public key:\t", pk)
    m = b'heliooooolo'
    print("message:\t", m)
    sig = Sign(m, sk, ec.curve)
    print("(r, s):\t\t", sig)
    f, vrfy = Verify(m, sig, pk, ec.curve)
    if f == True:
        print("verification passed.")
    else:
        print("verification failed.")
import tools as t
from collections import namedtuple

EllipticCurve = namedtuple('EllipticCurve', 'name p a b G n h l')

curve = EllipticCurve(
    'secp256k1',
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    a = 0,
    b = 7,
    G = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
         0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),#基点
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,#阶
    h = 1,
    l = 256 #256bit
)
    
def curvePoint(P, curve):
    x, y = P
    if t.fast_power(y, 2, curve.p) == (t.fast_power(x, 3, curve.p) + t.fast_mul(curve.a, x, curve.p) + curve.b) % curve.p:
        return True
    return False

def add_P_Q(P, Q, curve):
    if P == None:
        return Q
    if Q == None:
        return P
    assert curvePoint(P,curve) and curvePoint(Q,curve)
    [x1, y1] = P
    [x2, y2] = Q
    if P == Q:
        k = (t.fast_mul(3, t.fast_mul(x1, x1, curve.p), curve.p) + curve.a) * t.inverse(t.fast_mul(2, y1, curve.p), curve.p)
    else:
        k = (y1 - y2) * t.inverse(x1 - x2, curve.p)
    x3 = t.fast_mul(k, k, curve.p) - x1 - x2
    y3 = y1 + t.fast_mul(k, x3 - x1, curve.p)
    R = [x3 % curve.p, -y3 % curve.p]
    assert curvePoint(R, curve)
    return R

def calculate_dG(d, G, curve):
    """
    follows the double-and-add method to calculate d*G
    """
    assert curvePoint(G, curve)
    tmp = None
    while d:
        if d & 1:
            tmp = add_P_Q(tmp, G, curve)
        G = add_P_Q(G, G, curve)
        d >>= 1
    assert curvePoint(tmp, curve)
    return tmp
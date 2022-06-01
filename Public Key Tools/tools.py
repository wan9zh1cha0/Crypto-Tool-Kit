"""
this file provides some common tools
"""

import hashlib

def cal_sha1(x):
    s = hashlib.sha1(x)
    s = s.hexdigest()
    s = int(s, 16)
    return s

def fast_mul(x, y, p):
    """
    input: x, y, mod p
    output: x*y (mod p)
    """
    x %= p
    y %= p
    y = bin(y)[2:]  #convert y to binary string
    tmp = 0
    for i in range(len(y)):
        tmp = (tmp + tmp) % p
        if y[i] == '1':
            tmp = (tmp + x) % p
    return tmp
    
def fast_power(x, y, p):
    """
    input: x, y, mod p
    output: x^y (mod p)
    """
    x %= p
    y = bin(y)[2:]
    tmp = 1
    for i in range(len(y)):
        tmp = fast_mul(tmp, tmp, p)
        if y[i] == '1':
            tmp = fast_mul(tmp, x, p)
    return tmp

def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)
    
def inverse(x, p):
    assert x != 0
    if x < 0:
        return p - inverse(-x, p)
    else:
        s_, s = 0, 1
        t_, t = 1, 0
        r_, r = p, x
        while r_ != 0:
            q = r // r_
            s, s_ = s_, s - q * s_
            t, t_ = t_, t - q * t_
            r, r_ = r_, r - q * r_
        gcd, a, b = r, s, t
        assert gcd == 1
        assert fast_mul(x, a, p) == 1
        return a % p

if __name__ == '__main__':
    print(cal_sha1(b'hello'))
    print(inverse(3,5))
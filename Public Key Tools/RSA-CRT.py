'''
accelerate RSA decryption using Chinese Remainder Theorem (CRT)
'''

import tools

def factorize(n):
    '''
    compute p, q such that n = pq
    traverse odd numbers from 1 to sqrt(n) to find prime factors
    '''
    for i in range(3, int(pow(n, 0.5)) + 1, 2):
        if n % i == 0:
            p = i
            q = int(n / i)
            break
    return p, q

def RSA_CRT(c, d, p, q, n):
    '''
    RSA decryption using CRT
    input: p, q (prime factors of n), d (private exponent), c (ciphertext)
    output: m (plaintext)
    '''
    # step 2: compute m1, c1, d1, m2, c2, d2
    c1 = c % p
    d1 = d % (p - 1)
    c2 = c % q
    d2 = d % (q - 1)
    m1 = tools.fast_power(c1, d1, p)
    m2 = tools.fast_power(c2, d2, q)
    # step 3: compute m from m1, m2
    p_1 = tools.inverse(p, q)
    q_1 = tools.inverse(q, p)
    m = (q * q_1 * m1 + p * p_1 * m2) % n
    return m

if __name__ == '__main__':
    n = 3026533
    d = 2015347
    c = 152702
    # ------decryption directly------
    M = tools.fast_power(c, d, n)
    print("RSA decryption algorithm: m =", M)
    # ------decryption directly------
    
    # ------decryption with CRT------
    # factor n to get p, q (p, q are theoretically private keys, no need to factor)
    p, q = factorize(n)
    m = RSA_CRT(c, d, p, q, n)
    print("CRT accelerated algorithm: m =", m)
    # ------decryption with CRT------
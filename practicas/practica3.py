from sage.all import *

def UAB_generate_ElGamal_keys(nBits):
    if nBits % 64 != 0:
        return None

    p = Integer(0)

    while not p.is_prime():
        p = random_prime(pow(2, nBits), True, 3)

    Zp = GF(p)
    d = Integer(Zp(randint(1, p - 1)))
    alpha = primitive_root(p)

    k_priv = (p, alpha, d)

    c = power_mod(alpha, d, p)

    k_pub = (p, alpha, c)
    return [k_priv, k_pub]


def UAB_ElGamal_sign(k_priv, m, k=None):
    if len(k_priv) != 3:
        return None
    p = k_priv[0]
    k_prime = k  # Just to no make modifications over the input parameters
    if k_prime is None:
        is_invertible = False

        while not is_invertible:
            k_prime = Integer(randint(0, p - 1))
            is_invertible = k_prime.gcd(p - 1) == 1

    l = inverse_mod(k_prime, p - 1)
    r = power_mod(k_priv[1], k_prime, p)
    rd = r * k_priv[2]
    s = Integer(l * (m - rd)).mod(p - 1)

    return (r, s)


def UAB_ElGamal_verify(sig, k_pub, m):
    r, s = sig[0], sig[1]
    p = k_pub[0]
    if not (1 < r < p - 1):
        return False

    rs = power_mod(r, s, p)
    cs = power_mod(k_pub[2], r, p)
    v1 = Integer(cs * rs).mod(p)
    v2 = power_mod(k_pub[1], m, p)
    return v1 == v2

def UAB_extract_private_key(k_pub, m1, sig1, m2, sig2):
    if len(sig2) != 2 or len(sig1) != 2 or len(k_pub) != 3 or sig1[0] != sig2[0]:
        return -1

    p = k_pub[0]
    m2_minus_m1 = Integer(m2 - m1).mod(p - 1)
    s2_minus_s1 = Integer(sig2[1] - sig1[1])

    if s2_minus_s1.gcd(p - 1) != 1 or Integer(Integer(sig1[0]).gcd(p - 1) != 1):
        k = (m2_minus_m1 * s2_minus_s1).mod(p - 1)
        x = var("x")
        roots = solve_mod(x*sig1[0] == m1 - k, p - 1)
        if len(roots) == 0:
            return - 1
        return None, None, None

    else:
        s2_minus_s1 = inverse_mod(s2_minus_s1, p - 1)

        k = (m2_minus_m1 * s2_minus_s1).mod(p - 1)
        inverse_r = inverse_mod(sig1[0], p - 1)
        d = Integer((m1 - k * sig1[1]) * inverse_r).mod(p - 1)
        return (k_pub[0], k_pub[1], d)


    return (k_pub[0], k_pub[1], d)

def test_case_1a(name, num_tries, num_bits):
    [k_priv, k_pub] = UAB_generate_ElGamal_keys(num_bits)

    t1 = len(k_priv) == 3
    t2 = len(k_pub) == 3

    t3, t4, t5 = False, False, False
    if t1 & t2:
        t3 = k_pub[0] == k_priv[0]
        t4 = k_pub[1] == k_priv[1]
        t5 = k_pub[2] == power_mod(k_pub[1], k_priv[2], k_pub[0])

    print("Test", name + ":", t1 & t2 & t3 & t4 & t5)

def test_case_1b(name, k_priv, h, m, exp_r, exp_s):
    (r, s) = UAB_ElGamal_sign(k_priv, m, h)
    print(s, exp_s)
    print("Test", name + ":", (r == exp_r) & (s == exp_s))


def test_case_1c(name, sig, k_pub, m, exp_result):
    result = UAB_ElGamal_verify(sig, k_pub, m)
    print("Test", name + ":", (result == exp_result))


def test_case_2(name, k_pub, m1, sig1, m2, sig2, exp_k_priv):
    extracted_k_priv = UAB_extract_private_key(k_pub, m1, sig1, m2, sig2)
    print("Test", name + ":", exp_k_priv == extracted_k_priv)

def practica3():
    exp_k_priv = (1736419493, 423105914, 1439798331)
    k_pub = (1736419493, 423105914, 1388681513)
    m1, m2 = 4321, 1234
    sig1 = (1670801833, 813531998)
    sig2 = (1670801833, 1514976703)
    test_case_2("2.1", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = (3043480277, 949971850, 2984002184)
    k_pub = (3043480277, 949971850, 450506446)
    m1, m2 = 4321, 1234
    sig1 = (652612267, 1904199797)
    sig2 = (652612267, 716941154)
    test_case_2("2.2", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = (3081644339, 432364326, 231991852)
    k_pub = (3081644339, 432364326, 1072654913)
    m1, m2 = 4321, 1234
    sig1 = (2294114827, 97380409)
    sig2 = (2294114827, 744220606)
    test_case_2("2.3", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = (39929, 23050, 17872)
    k_pub = (39929, 23050, 3414)
    m1, m2 = 4321, 1234
    sig1 = (39612, 35145)
    sig2 = (39612, 38386)
    test_case_2("2.4", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = (38783, 10357, 9046)
    k_pub = (38783, 10357, 14443)
    m1, m2 = 4321, 1234
    sig1 = (12778, 29913)
    sig2 = (12778, 20620)
    test_case_2("2.5", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = (6203, 3754, 5115)
    k_pub = (6203, 3754, 540)
    m1, m2 = 4321, 1234
    sig1 = (3747, 3790)
    sig2 = (3747, 5435)
    test_case_2("2.6", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = -1
    k_pub = (1400337509, 1359471971, 45907697)
    m1, m2 = 4321, 4321
    sig1 = (639541257, 1115934695)
    sig2 = (639541257, 1115934695)
    test_case_2("2.7", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = -1
    k_pub = (2056635443, 830686420, 1880350451)
    m1, m2 = 4321, 1234
    sig1 = (1601254651, 1061368902)
    sig2 = (1601254651, 935119992)
    test_case_2("2.8", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = -1
    m1, m2 = 4321, 1234
    k_pub = (460730117, 91503345, 401055661)
    sig1 = (457648992, 18325781)
    sig2 = (457648992, 180721743)
    test_case_2("2.9", k_pub, m1, sig1, m2, sig2, exp_k_priv)

    exp_k_priv = -1
    m1, m2 = 4321, 1234
    k_pub = (3342796253, 1046051573, 77303856)
    sig1 = (1629150615, 2477614166)
    sig2 = (1462514112, 61485630)
    test_case_2("2.10", k_pub, m1, sig1, m2, sig2, exp_k_priv)

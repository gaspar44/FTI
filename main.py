from gcd import calculate_inverse
from sage.all import Integer

if __name__ == '__main__':
    e = Integer(73)
    p = Integer(211)
    q = Integer(509)

    calculate_inverse(e, p, q)

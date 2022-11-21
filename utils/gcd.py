from sage.all import *

def calculate_inverse(e,p,q):
    euler = euler_phi(p * q)
    print(inverse_mod(e, euler))



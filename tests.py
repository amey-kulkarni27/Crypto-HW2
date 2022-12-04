from sage.all import *

p = 31
E = EllipticCurve(GF(p), [2,3])
P = E(8, 29)
Q = E(30, 0)
print(discrete_log(Q, P))

# a, b, p, xg, yg, xf, yf = 9, 17, 23, 16, 5, 4, 5

# E = EllipticCurve(GF(p), [a, b])
# P = E(xg, yg)
# Q = E(xf, yf)

# print(discrete_log(Q, P, bounds=(2, 100)))
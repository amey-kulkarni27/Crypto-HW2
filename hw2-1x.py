from sage.all_cmdline import *
from lib import Q1a_e, Q1a_N, Q1a_top, Q1a_ell
R = ZZ['x']
x = R.gen()

N = Q1a_N
f = Q1a_e*Q1a_top + x

delta = 1 # degree
beta = 1/2
epsi = beta/3
gam = ceil(1/2 * N**(beta**2/delta-epsi))
assert(gam > 2**(512-Q1a_ell))
print(gam, 2**(512-Q1a_ell))
print(f)

m = ceil(beta**2 / (delta*epsi))
t = floor(delta*m*(1-beta)/beta)

# Hacky way of obtaining the full-list of coefs (including zeroes)
def coefs(fun, degree=(m+t)):
    assert(len(list(fun)) <= degree)
    c = list(fun+x**degree) # Add temporary monomial
    return c[:-1] # Remove the temporary monomial

base = []
for i in range(delta):
    for j in range(m):
        u = (x**i)*(N**(m-j))*(f**j)
        base.append(coefs(u(gam*x)))

for k in range(t):
    v = (x**k)*(f**m)
    base.append(coefs(v(gam*x)))

reduced = matrix(base).LLL()
# print("\n".join([str([hex(a) for a in v]) for v in reduced]))

hs = [sum([a*x**i/(gam**i) for i, a in enumerate(v)]) for v in reduced]
h = hs[0]

r = h.roots()[0][0]
# print("r=" + str(r))
p = gcd(f(r), N)
q = N / p
print(p * q == N)
print(is_prime(p))
print(is_prime(q))
print("p=" + hex(p))
print("q=" + hex(q))
d = Mod(Q1a_e, (p-1)*(q-1))**-1
d_p = Mod(d, p-1)
print("top=" + hex(Q1a_top))
print("d_p=" + hex(d_p))
print("d_p=" + str(d_p))

phi = N - (p + q - 1)
assert(Mod(Q1a_e*d, phi) == 1)
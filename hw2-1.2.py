from sage.all_cmdline import *
from lib import Q1b_e, Q1b_N, Q1b_low, Q1b_ell
R = ZZ['x']
x = R.gen()

e = Q1b_e
N = Q1b_N
ell = Q1b_ell
d_low = Q1b_low

k = 5 # figured this out through trial and error
assert(k > 1 and k < e)

# Compute s_low
temp = (e*d_low - 1)
exp = ell
while k % 2 == 0:
    if temp % 2 != 0:
        raise Exception("Invalid k")
    k = k // 2
    temp = temp // 2
    exp = exp - 1
temp = Mod(temp, 2**exp) / k
s_low = ((N+1) - temp).lift()

p_low = 1

def hensel_test(p, start):
    for i in range(start, 512):
        if not Mod(p**2 - s_low*p + N, 2**(i+1)).lift() == 0:
            return i
    return 512

ell = ell - 4

best = hensel_test(p_low, 0)
for j in range(1, ell):
    new_p = p_low + 2**j
    new_test = hensel_test(new_p, best)
    if new_test > best:
        best = new_test
        p_low = new_p

print("p_low=" + str(p_low))

print("# p_low valid :", (p_low * (s_low - p_low) - N) % 2**ell == 0)

# print("s_low=", s_low)
# print("# s_low valid :", Mod(e*d_low, 2**ell) == Mod(1 + 2*(N - s_low + 1), 2**ell))

a = (Mod(p_low, N) / (2**ell)).lift()

f = a + x

delta = 1 # degree
beta = 1/2
epsi = beta/7
gam = ceil(1/2 * N**(beta**2/delta-epsi))
assert(gam > 2**(512-ell))
print(gam, 2**(512-ell))
# print(f)

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

h = sum([a*x**i/(gam**i) for i, a in enumerate(reduced[0])])

r = h.roots()[0][0]
print("# roots :" + str(h.roots()))
p = gcd(f(r), N)
q = N / p
print("p=" + hex(p))
print("q=" + hex(q))
print("# p * q == N :", p * q == N)
d = Mod(e, (p-1)*(q-1))**-1
print("d_low=" + hex(d_low))
print("d=" + hex(d))
print("d=" + str(d))

phi = N - (p + q - 1)
assert(Mod(e*d, phi) == 1)

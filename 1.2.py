from sage.all import *
from sage.all_cmdline import *


Q1b_e=11
Q1b_N=99782296475367762991554702466834027785762146959282244349447067558948507818088463020008302295438212438020397878420372587653033133451714187803669507980265757197002882024023266792017388070989989766799763440990457833140536119028979673195871405378109589799741886674367807607580487633059145919648200328589050295041
Q1b_low=30814064615965857203285999135202987512924091511924776529297512750619577249252662554139489900577982873864104207301863696222009631090719
Q1b_ell=448


t_pow = 2**Q1b_ell

def is_root(x, s, N, pr_pow):
    v = x*x - s*x + N
    return ((v%pr_pow)==0)
    

def lift(r, s, N, pw):
    alpha = 2*r - s
    if alpha % 2 != 0:
        alpha_prime = 1 # since p is 2
        r_prime = r - alpha_prime * is_root(r, s, N, pow(2, pw))
        return [r_prime % pow(2, pw)]
    else:
        if(is_root(r, s, N, pow(2, pw)) and is_root(r + pow(2, pw-1), s, N, pow(2, pw))):
            return [r, r + pow(2, pw-1)]
        else:
            return []

    



# for k in range(1, 2):
for k in range(3, 5):
    k_inv = pow(k, t_pow-2, t_pow)
    s = k_inv * (Q1b_e*Q1b_low - 1) % t_pow - (Q1b_N + 1)
    s %= t_pow

    # s, Q1b_N = 2, 1
    roots = []
    for pw in range(1, Q1b_ell + 1): # find the roots for 2^pw
        new_roots = []
        if pw == 1:
            if is_root(0, s, Q1b_N, 2):
                roots.append(0)
            if is_root(1, s, Q1b_N, 2):
                roots.append(1)
        else:
            for root in roots: # lift root of pw-1 to pw
                new_roots = lift(root, s, Q1b_N, pw)
                new_roots.extend(new_roots)
            if len(new_roots) == 0:
                print("None for ", k)
                roots = []
                break
            roots = new_roots
    roots = (list(set(roots)))
    for root in roots:
        assert(is_root(root, s, Q1b_N, pow(2, Q1b_ell)))
        print(root.bit_length())
        a = (root * pow(t_pow, Q1b_N-2, Q1b_N)) % Q1b_N

        R = ZZ['x']
        x = R.gen()
        f = a*Q1b_e + x
        delta = 1 # degree
        beta = 1/2
        epsi = beta/3
        gam = ceil(1/2 * Q1b_N**(beta**2/delta-epsi))
        assert(gam > 2**(512-Q1b_ell))
        print(gam, 2**(512-Q1b_ell))
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
                u = (x**i)*(Q1b_N**(m-j))*(f**j)
                base.append(coefs(u(gam*x)))

        for k in range(t):
            v = (x**k)*(f**m)
            base.append(coefs(v(gam*x)))

        reduced = matrix(base).LLL()
        # print("\n".join([str([hex(a) for a in v]) for v in reduced]))

        hs = [sum([a*x**i/(gam**i) for i, a in enumerate(v)]) for v in reduced]
        h = hs[0]
        if len(h.roots()) == 0:
            continue
        r = h.roots()[0][0]
        # print("r=" + str(r))
        print("HIiuh")
        p = gcd(f(r)*t_pow, Q1b_N)
        q = Q1b_N / p
        print(p * q == Q1b_N)



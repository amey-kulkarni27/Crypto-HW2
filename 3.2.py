from sage.all import *
import socket
from time import time

st = time()
seed = 10149914677518896998
SIZE = 2048
Q3b_pp=(288896942194479865787066238983886113210, 204469037238514630544159596635850262171, 303233436581542225137301039935865399829, 253081425216046329813149694764493563485, 9527753076860320747832247305074494887, 303233436581542225113915293011921183507, 1)
a, b, p, xg, yg, n, h = Q3b_pp

def is_prime(x):
    i = 2
    while i * i <= x:
        if(x % i == 0):
            return False
        i += 1
    return True

def get_primes(lim):
    cur = 1
    res = [2]
    p = 3
    while cur <= lim:
        if(is_prime(p)):
            res.append(p)
            cur *= p
        p += 2
    return res

def crt(ai):
    P = 1
    for pi in ai.keys():
        P *= pi

    ans = 0
    for p, a in ai.items():
        y = P // p
        z = pow(y, p-2, p)
        ans += (a * y * z)
    return ans


cur = 1
ai = dict()
primes = get_primes(p)
print(primes)


for pr in primes:
    E = EllipticCurve(GF(p), [a,b])
    bdash = 0
    while True:
        E_dash = EllipticCurve(GF(p), [a,bdash])
        K = E_dash.order()
        if(K % pr == 0):
            break
        bdash += 1
    P_gen = (E_dash.gens()[0])
    ord = P_gen.order() // pr
    P_dash = ord * P_gen
    assert(P_dash.order() == pr)
    # print(K)
    # P = E(xg, yg)
    # break
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
    #     csock.connect(("lasecpi1.epfl.ch", 8888))
    #     args = [str(seed), format(P[0], "x"), format(P[1], "x")]
    #     payload = " ".join(args) + "\n"
    #     csock.send(payload.encode()) # call the oracle
    #     chunk1: bytes = csock.recv(SIZE) # read a chunk of SIZE bytes
    #     res = chunk1
    #     x_Q, y_Q = res.decode().split(" ")
    #     # print(int(x_Q, 16), int(y_Q, 16))
    #     if x_Q == "inf" and y_Q == "inf":
    #         # do something knowing Q = (oo)
    #         print("Inf")
    #     else:
    #         x_Q, y_Q = int(x_Q, 16), int(y_Q, 16)
    #         # do something with the integers
    #         print(x_Q, y_Q)
    #         # socket resources are released when exiting the context
    
    # Q_dash = E_dash(x_Q, y_Q)

    # Point at infinity is represented as
    p_inf = E_dash(0, 1, 0)

    Q_dash = P_dash
    # print(pr)
    for i in range(pr):
        if Q_dash == P_dash * i:
            ai[pr] = i

ans = crt(ai)
print(ans)
print(ans % p)
    

en = time()
print(en - st)
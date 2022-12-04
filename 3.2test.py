from sage.all import *
import socket

seed = 10149914677518896998
SIZE = 2048
Q3b_pp=(288896942194479865787066238983886113210, 204469037238514630544159596635850262171, 303233436581542225137301039935865399829, 253081425216046329813149694764493563485, 9527753076860320747832247305074494887, 303233436581542225113915293011921183507, 1)
a, b, p, xg, yg, n, h = Q3b_pp
sk = 82865960128030221958337605666122389629

E = EllipticCurve(GF(p), [a,b])
P_gen = (E.gens()[0])
# P_gen = E(xg, yg)
Q_calc = sk * P_gen
p_inf = E(0, 1, 0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as csock:
    csock.connect(("lasecpi1.epfl.ch", 8888))
    args = [str(seed), format(int(P_gen[0]), "x"), format(int(P_gen[1]), "x")]
    payload = " ".join(args) + "\n"
    csock.send(payload.encode()) # call the oracle
    chunk1: bytes = csock.recv(SIZE) # read a chunk of SIZE bytes
    res = chunk1
    x_Q, y_Q = res.decode().split(" ")
    # print(int(x_Q, 16), int(y_Q, 16))
    if x_Q == "inf" and y_Q == "inf":
        # do something knowing Q = (oo)
        Q_dash = p_inf
    else:
        x_Q, y_Q = int(x_Q, 16), int(y_Q, 16)
        # do something with the integers
        Q_dash = E(x_Q, y_Q)

print(Q_dash == Q_calc)

# rems = {2: 1, 3: 1, 5: 4, 7: 3, 11: 10, 13: 0, 17: 12, 19: 0, 23: 12, 29: 22, 31: 6, 37: 35, 41: 31, 43: 32, 47: 24, 53: 20, 59: 21, 61: 56, 67: 24, 71: 55, 73: 70, 79: 78, 83: 74, 89: 48, 97: 85, 101: 4, 103: 69}
# for pr, r in rems.items():
#     assert(sk%pr == r)
from sage.all import *
Q3a_pp=(0, 341013125595457660222226053548539955775, 428843212935877404563984956305784700927, 145426492073771163961791976518260032744, 72653657345595385753799562992953078062, 35736934411323117046998746358815391744, 12)
Q3a_pk=(349462162449660550268911336675940579952, 8072683805654195904207862259520573005)

a, b, p, xg, yg, n, h = Q3a_pp
xf, yf = Q3a_pk
# a, b, p, xg, yg, xf, yf = 9, 17, 23, 16, 5, 4, 5
xnew, ynew = xg, yg

E = EllipticCurve(GF(p), [a,b])
P = E(xg, yg)
Q = E(xf, yf)
fr = (discrete_log(Q, P, operation='+'))
print(fr)
print(fr*P == Q)
# print(E.order() == h*n)

# for skb in range(1, 100):
#     xnew, ynew = f(xnew, ynew)
#     print(skb, xnew, ynew)
#     if xnew == xf and ynew == yf:
#         break


# for pr, i in pfs.items():
#     print(pow(pr, i))
#     for k in range(pow(pr, i)):
#         if k * P == Q:
#             print(k)
#             break
    
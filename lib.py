import re

def myeval(s):
    import ast
    try:
        return ast.literal_eval(s)
    except Exception:
        return s

with open("353055/353055-params.txt","r") as f:
    for l in f:
        g = re.findall("^(Q[A-Za-z0-9_]+)=(.+)\n?$",l)
        assert(len(g) < 2)
        if len(g) == 0:
            continue
        globals()[g[0][0]] = myeval(g[0][1])
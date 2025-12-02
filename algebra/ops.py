from itertools import product

# 共役
def conjugate(G, g, x):
    return G.multiply(G.multiply(g, x), G.inverse(g))

# 共役写像
def conjugation_map(G, g):
    return {x: conjugate(G, g, x) for x in G.elements}

# 交換子[g1, g2] = g1g2g1^(-1)g2^(-1)
def commutator(G, a, b):
    return G.multiply(G.multiply(a, b), G.multiply(G.inverse(a), G.inverse(b)))

# 中心
def center(G):
    elems = G.elements
    Z = []
    for x in elems:
        if all(G.multiply(x, y) == G.multiply(y, x) for y in elems):
            Z.append(x)
    return Z

# 交換子部分群[G, G]
def commutator_subgroup(G):
    elems = G.elements
    comms = {commutator(G, a, b) for a, b in product(elems, repeat=2)}
    return comms
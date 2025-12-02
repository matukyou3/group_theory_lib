from algebra.ops import center
from algebra.theory import  Inn, Auto
from groups.dihedral import DihedralGroup

G = DihedralGroup(9)
for g in G.elements:
    print(g.word)

print(center(G))
print(len(Inn(G)))
print(Auto(G))
print(len(Auto(G)))
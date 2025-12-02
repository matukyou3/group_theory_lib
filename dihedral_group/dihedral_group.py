# s：鏡映
# r：回転
# R^n = e
# S^2 = e
# RS = SR^(-1)

class DiherdralElement:
    def __init__(self, r=0, s=False, n=1):
        self.r = r % n
        self.s = s
        self.n = n
        

    def __repr__(self):
        return f"S·R^{self.r}" if self.s else f"R^{self.r}"
    
    def __eq__(self, other):
        return (
            isinstance(other, DiherdralElement) and
            self.n == other.n and
            self.s == other.s and
            self.r == other.r
        )
    
    def __hash__(self):
        return hash((self.r, self.s, self.n))
    
class DiherdralGroup:
    # 群構造定義
    def __init__(self, n):
        self.n = n

        # 元書き下し
        self.elements = []
        for k in range(n):
            self.elements.append(DiherdralElement(k, False, n))
        for k in range(n):
            self.elements.append(DiherdralElement(k, True, n))

        # 単位元
        self.e = DiherdralElement(0, False, n)

    # 群演算定義
    def multiply(self, a, b):
        n = self.n
        # (R^a)(R^b) = R^(a+b)
        if not a.s and not b.s:
            return DiherdralElement(a.r + b.r, False, n)
    
        #(R^a)(S R^b) = S R^(b-a)
        if not a.s and b.s:
            return DiherdralElement(b.r - a.r, True, n)
        
        #(S R^a)(R^b) = S R^(a+b)
        if a.s and not b.s:
            return DiherdralElement(a.r + b.r, True, n)
        
        #(S R^a)(S R^b) = R^(b-a)
        if a.s and b.s:
            return DiherdralElement(b.r -a.r, False, n)

    # 逆元
    def inverse(self, a):
        n = self.n
        if not a.s:
            return DiherdralElement(-a.r, False, n)
        else:
            return DiherdralElement(a.r, True, n)
    
    # 共役 φ_g(x) → g x g^(-1)
    def conjugate(self, g, x):
        return self.multiply(self.multiply(g, x), self.inverse(g))
    
    # 中心
    def center(self):
        Z = []
        for z in self.elements:
            if all(self.multiply(z, g) == self.multiply(g, z) for g in self.elements):
                Z.append(z)
            return Z
        
    # 内部自己同型
    def inner_automorphism(self, g):
        return {x: self.conjugate(g, x) for x in self.elements}
        
    # Inn(G)の計算
    def compute_inn_group(self):
        """Return list of distinct inner automorphisms."""
        autos = []
        reps = []  # representative elements

        for g in self.elements:
            phi_g = self.inner_automorphism(g)
            if all(phi_g != aut for aut in autos):
                autos.append(phi_g)
                reps.append(g)

        return autos, reps


D=DiherdralGroup(n=6)
print(D.elements)
autos, reps = D.compute_inn_group()
print(len(autos))
print(reps)

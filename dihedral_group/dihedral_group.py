from itertools import product
import math

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
            self.r == other.r and
            self.s == other.s and
            self.n == other.n
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

    # Aut(G)の計算
    def compute_aut_group(self):
        autos = []
        reps = []

        elems = self.elements
        rot = []
        refl = []
        for elem in elems:
            # 回転の場合
            if not elem.s:
                if math.gcd(elem.r, self.n) == 1:
                    rot.append(elem)
            
            # 鏡映を含む場合
            else:
                refl.append(elem)

        print(rot)
        print(refl)
        # 回転と鏡映のペアの写像の像を計算する
        for img_r, img_s in product(rot, refl):
            
            phi = {}

            for x in self.elements:
                if not x.s:
                    # x = r^kのケース
                    # 鏡映なし
                    out = self.e
                    power = self.e
                    for _ in range(x.r):
                        power = self.multiply(power, img_r)
                    phi[x] = self.multiply(out, power)

                else:
                    out = img_s
                    power = self.e
                    for _ in range(x.r):
                        power = self.multiply(power, img_r)
                    phi[x] = self.multiply(out, power)

            if len(set(phi.values())) != len(self.elements):
                continue
            ok = True
            for x in self.elements:
                for y in self.elements:
                    if phi[self.multiply(x,y)] != self.multiply(phi[x], phi[y]):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
                        
            if phi not in autos:
                autos.append(phi)
                reps.append((img_r, img_s))
        
        return autos, reps


D=DiherdralGroup(n=5)
autos, reps = D.compute_aut_group()

print(len(autos))
print(reps)
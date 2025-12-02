from itertools import product
import math
from algebra import Group, FiniteGroup, GroupElement

# s：鏡映
# r：回転
# R^n = e
# S^2 = e
# RS = SR^(-1)

class DihedralElement(GroupElement):
    def __init__(self, r=0, s=False, n=1, r_gen=None, s_gen=None):
        self.r = r % n
        self.s = s
        self.n = n
        self.r_gen = r_gen
        self.s_gen = s_gen

        if self.s:
            self.word = [self.s_gen] + [self.r_gen]*self.r
        else:
            self.word = [self.r_gen]*self.r

        

    def __repr__(self):
        return f"S·R^{self.r}" if self.s else f"R^{self.r}"
    
    def __eq__(self, other):
        return (
            isinstance(other, DihedralElement) and
            self.r == other.r and
            self.s == other.s and
            self.n == other.n
        )
    
    def __hash__(self):
        return hash((self.r, self.s, self.n))
    
class DihedralGroup(FiniteGroup):
    # 群構造定義
    def __init__(self, n):
        self.n = n
        elems = []
        self.r_gen = DihedralElement(1, False, n)
        self.s_gen = DihedralElement(0, True, n)

        for k in range(self.n):
            elems.append(DihedralElement(k, False, self.n, r_gen=self.r_gen, s_gen=self.s_gen))
        for k in range(self.n):
            elems.append(DihedralElement(k, True, self.n, r_gen=self.r_gen, s_gen=self.s_gen))
        self._elements = elems
    
    # 生成元
    @property
    def generators(self):
        return [self.r_gen, self.s_gen]
    
    # 群演算定義
    def multiply(self, a, b):
        n = self.n
        # (R^a)(R^b) = R^(a+b)
        if not a.s and not b.s:
            return DihedralElement(a.r + b.r, False, n, r_gen=self.r_gen, s_gen=self.s_gen)
    
        #(R^a)(S R^b) = S R^(b-a)
        if not a.s and b.s:
            return DihedralElement(b.r - a.r, True, n, r_gen=self.r_gen, s_gen=self.s_gen)
        
        #(S R^a)(R^b) = S R^(a+b)
        if a.s and not b.s:
            return DihedralElement(a.r + b.r, True, n, r_gen=self.r_gen, s_gen=self.s_gen)
        
        #(S R^a)(S R^b) = R^(b-a)
        if a.s and b.s:
            return DihedralElement(b.r -a.r, False, n, r_gen=self.r_gen, s_gen=self.s_gen)

    # 単位元
    @property
    def identity(self):
        return DihedralElement(0, False, self.n, r_gen=self.r_gen, s_gen=self.s_gen)
    

    # 逆元
    def inverse(self, a):
        n = self.n
        if not a.s:
            return DihedralElement(-a.r, False, n, r_gen=self.r_gen, s_gen=self.s_gen)
        else:
            return DihedralElement(a.r, True, n, r_gen=self.r_gen, s_gen=self.s_gen)
    
    @property
    def elements(self):
        return self._elements


    # 共役 φ_g(x) → g x g^(-1)
    def conjugate(self, g, x):
        return self.multiply(self.multiply(g, x), self.inverse(g))
    
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

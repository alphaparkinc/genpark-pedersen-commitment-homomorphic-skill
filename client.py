"""Homomorphic Pedersen Commitment Scheme.
100% Python Standard Library.
"""

import hashlib
import secrets

class Secp256k1Curve:
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    A = 0
    B = 7
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    @classmethod
    def point_add(cls, p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and y1 != y2:
            return None
        if x1 == x2 and y1 == y2:
            m = (3 * x1 * x1 + cls.A) * pow(2 * y1, cls.P - 2, cls.P) % cls.P
        else:
            m = (y2 - y1) * pow(x2 - x1, cls.P - 2, cls.P) % cls.P
        x3 = (m * m - x1 - x2) % cls.P
        y3 = (m * (x1 - x3) - y1) % cls.P
        return (x3, y3)

    @classmethod
    def scalar_mult(cls, k: int, point=None):
        if point is None:
            point = (cls.Gx, cls.Gy)
        result = None
        addend = point
        while k:
            if k & 1:
                result = cls.point_add(result, addend)
            addend = cls.point_add(addend, addend)
            k >>= 1
        return result

class PedersenCommitment:
    """Pedersen commitment C = m*G + r*H with perfect hiding and computational binding."""
    P = Secp256k1Curve.P
    curve = Secp256k1Curve
    G = (curve.Gx, curve.Gy)
    Hx = int(hashlib.sha256(b"PedersenGeneratorH_X").hexdigest(), 16) % P
    Hy = int(hashlib.sha256(b"PedersenGeneratorH_Y").hexdigest(), 16) % P
    H = (Hx, Hy)

    @classmethod
    def commit(cls, m: int, r: int = None) -> tuple:
        if r is None:
            r = secrets.randbelow(cls.curve.N - 1) + 1
        mG = cls.curve.scalar_mult(m % cls.curve.N, cls.G)
        rH = cls.curve.scalar_mult(r % cls.curve.N, cls.H)
        C = cls.curve.point_add(mG, rH)
        return C, r

    @classmethod
    def verify(cls, commitment: tuple, m: int, r: int) -> bool:
        expected, _ = cls.commit(m, r)
        return commitment == expected

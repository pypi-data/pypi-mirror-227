from collections import namedtuple as _namedtuple

_Residueclass = _namedtuple('_Residueclass', ['representative', 'modulus'])
class Residueclass(_Residueclass):
    def __new__(cls, representative, modulus):
        if type(modulus) is cls:
            raise TypeError
        if type(representative) is cls:
            modulus = cls._gcd(representative.modulus, modulus)
            representative = representative.representative
        representative = cls._mod(
            representative,
            modulus,
            strict=True,
        )
        return _Residueclass.__new__(
            cls,
            representative=representative,
            modulus=modulus,
        )
    def __bool__(self):
        return bool(self.representative)
    def __getitem__(self, key):
        return self.representative + (key * self.modulus)
    def __iter__(self):
        raise NotImplementedError
    def __contains__(self, other):
        other = type(self)(other, self.modulus)
        return self == other
    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self._tuple() == other._tuple()
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return self._tuple().__hash__()
    def __add__(self, other):
        other = self._new(other)
        representative = self.representative + other.representative
        modulus = self._gcd(self.modulus, other.modulus)
        return type(self)(
            representative=representative,
            modulus=modulus,
        )
    def __radd__(self, other):
        return self._new(other) + self
    def __neg__(self):
        return type(self)(
            representative=-self.representative,
            modulus=self.modulus,
        )
    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return other + (-self)
    def __mul__(self, other):
        other = self._new(other)
        representative = self.representative * other.representative
        modulus = self._gcd(self.modulus, other.modulus)
        return type(self)(
            representative=representative,
            modulus=modulus,
        )
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        return self * self._new(other).reciprocal()
    def __pow__(self, other):
        exp = self._int(other)
        if exp >= 0:
            factor = self
        else:
            factor = self.reciprocal()
        ans = 1
        for i in range(abs(exp)):
            ans *= factor
        return ans
    def _new(self, other):
        if type(self) is type(other):
            return other
        return type(self)(
            representative=other,
            modulus=self.modulus,
        )
    def _tuple(self):
        return (self.representative, self.modulus)
    @classmethod
    def _int(cls, x, /):
        ans = int(x)
        if x == ans:
            return ans
        else:
            raise ValueError
    @classmethod
    def _zeroDivisionError(cls):
        raise ZeroDivisionError
    @classmethod
    def _fulldiv(cls, x, y, /):
        q, r = divmod(x, y)
        if r:
            raise ValueError
        else:
            return q
    @classmethod
    def _divmod(cls, x, y, /):
        if not y:
            cls._zeroDivisionError()
        return divmod(x, y)
    @classmethod
    def _modzero(cls, x, /, *, strict):
        if strict:
            cls._zeroDivisionError()
        return x
    @classmethod
    def _mod(cls, x, y, **kwargs):
        if not y:
            return cls._modzero(x, **kwargs)
        return cls._divmod(x, y)[1]
    @classmethod
    def _gcd(cls, x, y):
        return cls._gcd_ext(x, y)[0]
    @classmethod
    def _gcd_ext(cls, x, y):
        g, h = 0, 1
        while y:
            q, r = cls._divmod(x, y)
            x, y = y, r
            g, h = h, g + (-(q * h))
        return x, g
    def reciprocal(self):
        representative, modulus = self._tuple()
        gcd, ext = self._gcd_ext(modulus, representative)
        modulus = self._fulldiv(modulus, gcd)
        gcd, ext = self._gcd_ext(modulus, representative)
        #ext = self._fulldiv(ext, gcd)
        return type(self)(
            representative=ext,
            modulus=modulus,
        )
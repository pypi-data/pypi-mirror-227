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
        raise NotImplementedError
    def __iter__(self):
        raise NotImplementedError
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
    def _mod(cls, x, y, strict=True):
        if y:
            return x % y
        elif strict:
            raise ZeroDivisionError
        else:
            return x 
    @classmethod
    def _gcd(cls, x, y):
        while y:
            x, y = y, cls._mod(
                x, 
                y,
                strict=True,
            )
        return x
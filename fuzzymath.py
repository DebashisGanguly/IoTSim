import math
from decimal import Decimal

def fAlmostEqual(a, b, rtol=1.0000000000000001e-05, atol=1e-08):
    """Checks if the given floats are almost equal. Uses the algorithm
    from numpy.allclose."""
    return math.fabs(Decimal(a) - b) <= (atol + rtol * math.fabs(b))

def fuzzyFloor(v):
    """Returns the floor of the given number, unless it is equal to its
    ceiling (within floating point error)."""
    floor = math.floor(v)
    if fAlmostEqual(floor+1, v):
        return floor+1
    return floor
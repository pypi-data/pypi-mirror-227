from sympy import *
from nbag import construct
import sympy


def deferredVector(name=None, **assumptions):
    return construct(sympy.DeferredVector, name, **assumptions)

def dummy(dummy_index=None, name=None, **assumptions):
    return construct(sympy.Dummy, name, dummy_index, **assumptions)

def matrixSymbol(n, m, name=None):
    return construct(sympy.MatrixSymbol, name, n, m)

def symbol(name=None, **assumptions):
    return construct(sympy.Symbol, name, **assumptions)

def wild(exclude=(), properties=(), name=None, **assumptions):
    return construct(sympy.Wild, name, exclude, properties, **assumptions)


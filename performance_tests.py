from random import randint, choice
from functools import lru_cache
from src.memoize import memoize
from time import perf_counter
from math import fmod
import numpy as np

@memoize
def j(n):
    n
    for i in range(5000):
        i

@lru_cache
def l(n):
    n
    for i in range(5000):
        i


start = perf_counter()
for i in range(10000):
    l(1)
print(perf_counter() - start)


start = perf_counter()
for i in range(10000):
    j(1)
print(perf_counter() - start)

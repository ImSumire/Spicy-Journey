"""Perlin Noise with a very simple use
	Adapted from Stefan Gustavson's Java implementation described in the pdf 'simplexnoise.pdf'

	https://en.wikipedia.org/wiki/Ken_Perlin

	Why Simplex Noise and not Perlin Noise ?

	Complexity :
		https://en.wikipedia.org/wiki/Perlin_noise Complexity : O(2^N)
		https://en.wikipedia.org/wiki/Simplex_noise Complexity : O(N)
		Lower computational complexity, cost and fewer multiplications makes the a very fast computing speed

	Version : 0.2"""

from math import sqrt
from random import randint, shuffle, seed

__version__ = 0.2

SEED = 10000000

# Gradient Vectors
grad_vect = [
    [1, 1, 0],
    [-1, 1, 0],
    [1, -1, 0],
    [-1, -1, 0],
    [1, 0, 1],
    [-1, 0, 1],
    [1, 0, -1],
    [-1, 0, -1],
    [0, 1, 1],
    [0, -1, 1],
    [0, 1, -1],
    [0, -1, -1],
    [1, 1, 0],
    [0, -1, 1],
    [-1, 1, 0],
    [0, -1, -1],
]


permutation_length = 512


def new_seed():
    global SEED, permutation
    seed(None)  # Remove the seed
    SEED = randint(10e6, 99999999)  # Create a new seed
    seed(SEED)  # Set the new seed

    p = [i for i in range(permutation_length)]
    shuffle(p)
    permutation = p * 2


def get_seed():
    return SEED


def noise(x, y):
    """
    2D Perlin simplex noise.

    Return a floating point value from -1 to 1 for the given x, y coordinate.
    The same value is always returned for a given x, y pair unless the
        permutation table changes (see randomize above).
    """

    # Simplex Constants
    f = 0.3660254
    g = 0.2113249

    s = (x + y) * f
    i = int(x + s)
    j = int(y + s)
    t = (i + j) * g
    x0 = x - (i - t)
    y0 = y - (j - t)

    if x0 > y0:
        i1 = 1
        j1 = 0
    else:
        i1 = 0
        j1 = 1

    x1 = x0 - i1 + g
    y1 = y0 - j1 + g
    x2 = x0 + g * 2.0 - 1.0
    y2 = y0 + g * 2.0 - 1.0

    ii = int(i) % permutation_length
    jj = int(j) % permutation_length
    gi0 = permutation[ii + permutation[jj]]
    gi1 = permutation[ii + i1 + permutation[jj + j1]]
    gi2 = permutation[ii + 1 + permutation[jj + 1]]

    tt = .5 - x0 * x0 - y0 * y0

    if tt > 0:
        g = grad_vect[gi0 % 12]
        noise = (tt * tt * tt * tt) * (g[0] * x0 + g[1] * y0)
    else:
        noise = 0.0

    tt = 0.5 - x1 * x1 - y1 * y1
    if tt > 0:
        g = grad_vect[gi1 % 12]
        noise += (tt * tt * tt * tt) * (g[0] * x1 + g[1] * y1)

    tt = 0.5 - x2 * x2 - y2 * y2
    if tt > 0:
        g = grad_vect[gi2 % 12]
        noise += (tt * tt * tt * tt) * (g[0] * x2 + g[1] * y2)

    return noise * 50.0

"""
    ✓ (2, 1)[b > c]
    ✓ (b > c) and 2 or 1
    ✗ a = 1 if b > c else 2

    ✓ list.append()
    ✗ list += [obj]

    ✓ str(int(number))
    ✗ str(round(i))

    ✓ '%s, %s, %s' % (a, b, c)
    ✗ f'{a}, {b}, {c}'
    ✗ '{}, {}, {}'.format(a, b, c)
"""

from time import perf_counter

a, b, c = 1, 2, 3

start = perf_counter()
for i in range(10000000):
    f"{a}, {b}, {c}"
print(perf_counter() - start)

start = perf_counter()
for i in range(10000000):
    "{}, {}, {}".format(a, b, c)
print(perf_counter() - start)

start = perf_counter()
for i in range(10000000):
    "%s, %s, %s" % (a, b, c)
print(perf_counter() - start)

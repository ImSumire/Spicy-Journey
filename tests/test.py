"""
    ✓ (2, 1)[b > c]
    ✓ (b > c) and 2 or 1
    ✗ a = 1 if b > c else 2

    ✓ list.append()
    ✗ list += [obj]

    ✓ str(int(number))
    ✗ str(round(number))

    ✓ '%s, %s, %s' % (a, b, c)
    ✗ f'{a}, {b}, {c}'
    ✗ '{}, {}, {}'.format(a, b, c)

    ✓ a < b
    ✗ a <= b
"""

from time import perf_counter, time

a = 1
b = 4

start = perf_counter()
for i in range(10000000):
    a < b
print(perf_counter() - start)

start = perf_counter()
for i in range(10000000):
    a <= b
print(perf_counter() - start)

#!/usr/bin/python3
import math

vals = []
print('Input values separated by spaces as floats (not as percentages):')
vals = [float(i) for i in input().split()]


def test(v: [float], k: int):
    tv = []
    for i in v:
        tv.append({i*k:int(i*k)})
        if int(i * k) != i * k:
            return False
    return True


k = 1
while not test(vals, k):
    k += 1

print(k)

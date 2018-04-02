#!/usr/bin/python3
def a(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return a(n - 1) + a(n - 2) + 1


found = False
c = 0
if __name__ == '__main__':
    while not found:
        c += 1
        if a(c) > 1000000:
            break
    print('a({}) = {}'.format(c, a(c)))

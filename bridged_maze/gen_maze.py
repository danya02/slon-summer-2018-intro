#!/usr/bin/python3
import random

x = int(input('width: '))
y = int(input('height: '))
prob_wall = float(input('probability of point being impassable (0~1): '))
prob_bridge = float(input('probability of point being a bridge (0~1): '))

e = ['o' for i in range(x)]
m = [e.copy() for i in range(y)]
for cy in range(y):
    for cx in range(x):
        if random.random() < prob_wall:
            try:
                m[cx][cy] = '.'
            except IndexError:
                pass
        elif random.random() < prob_bridge:
            try:
                m[cx][cy] = 'x'
            except IndexError:
                pass
m[0][y-1] = 'o'
m[x - 1][0] = 'o'
if __name__ == '__main__':
    with open('maze.txt', 'w') as o:
        o.write('\n'.join([''.join(i) for i in m]))

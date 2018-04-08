#!/usr/bin/python3
import sys

sys.setrecursionlimit(2 ** 30)
from pypaths import astar


class Infty(float):
    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return isinstance(other, Infty)

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False


class BridgedMaze:
    def __init__(self, impassable='.', bridge='x', free='o'):
        self.maze = [[]]
        self.impassable = impassable
        self.bridge = bridge
        self.free = free
        self.x = 0
        self.y = 0
        self.sx = 0
        self.sy = 0
        self.ex = 0
        self.ey = 0
        self.diagonals_allowed = False

    @staticmethod
    def distance(a: (int, int), b: (int, int)) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def load(self, filename: str) -> None:
        self.maze = []
        with open(filename) as o:
            for i in o:
                self.maze += [list(i.split('\n')[0])]
        self.y = len(self.maze)
        self.x = len(self.maze[0])
        self.sx = self.x-1
        self.sy = 0
        self.ex = 0
        self.ey = self.y - 1

    def solve(self) -> list:
        search = astar.pathfinder(self.neighbors, self.distance, self.cost)
        return search((self.sy, self.sx), (self.ey, self.ex))

    def print(self) -> None:
        maze = self.maze.copy()
        try:
            maze[self.sy][self.sx] = 'S'
            maze[self.ey][self.ex] = 'E'
        except IndexError:
            pass
        print('\n'.join([''.join(i) for i in maze]))

    def solution_print(self):
        self.load('maze.txt')
        print('This maze is:')
        self.print()
        s = self.solve()
        try:
            s[0] > 1
        except TypeError:
            print('This maze cannot be solved! {}'.format(s))
            exit()
        if s[0] > 1024 * m.x * m.y:
            print('This maze cannot be solved! ({})'.format(s[0]))
        else:
            print('This maze can be solved if {} bridges are passed.'.format(s[0]))
            print('The path is:')
            x = m.x - 1
            y = m.y - 1

            def o(a: str) -> None:
                print(a, '-', end=' ')

            o('enter')
            s[1].pop(0)
            wtf = False
            for i in s[1]:
                if i[0] < y:
                    if i[1] == x:
                        o('south')
                    elif i[1] < x:
                        o('southwest')
                    elif i[1] > x:
                        o('southwest')
                elif i[0] == y:
                    if i[1] > x:
                        o('east')
                    elif i[1] < x:
                        o('west')
                    elif i[1] == x:
                        o('wait (WTF?!)')
                        wtf += 1
                elif i[0] > y:
                    if i[1] == x:
                        o('north')
                    elif i[1] < x:
                        o('northeast')
                    elif i[1] > x:
                        o('northwest')
                else:
                    o('t-port to {} (WTF?!)'.format(i))
                    wtf += 1
                x = i[1]
                y = i[0]
            print('exit')
            if wtf:
                print('WARNING: {} abnormal route conditions detected. The answer above is probably incorrect. What a '
                      'Terrible Failure!'.format(wtf))

    def cost(self, a: (int, int), b: (int, int)) -> float:
        try:
            if self.maze[a[1]][a[0]] == self.bridge:
                return 1
            elif self.maze[b[1]][b[0]] == self.bridge:
                return 0
            elif self.maze[a[1]][a[0]] == self.impassable:
                return Infty(self.x * self.y * 18446744073709551615)
            elif self.maze[b[1]][b[0]] == self.impassable:
                return Infty(self.x * self.y * 18446744073709551615)
            else:
                return 0
        except IndexError:
            return Infty(self.x * self.y * 340282366920938463463374607431768211455)

    def neighbors(self, p: (int, int)) -> [(int, int)]:
        n = (p[0], p[1] - 1)
        ne = (p[0] + 1, p[1] - 1)
        e = (p[0] + 1, p[1])
        se = (p[0] + 1, p[1] + 1)
        s = (p[0], p[1] + 1)
        sw = (p[0] - 1, p[1] + 1)
        w = (p[0] - 1, p[1])
        nw = (p[0] - 1, p[1] - 1)
        ns = [n, ne, e, se, s, sw, w, nw]

        def rem(v: (int, int)) -> None:
            try:
                ns.remove(v)
            except ValueError:
                pass

        if p[1] == 0:
            rem(n)
            rem(ne)
            rem(nw)
        if p[1] == self.y - 1:
            rem(s)
            rem(se)
            rem(sw)
        if p[0] == 0:
            rem(w)
            rem(sw)
            rem(nw)
        if p[0] == self.x - 1:
            rem(e)
            rem(se)
            rem(ne)
        if not self.diagonals_allowed:
            rem(ne)
            rem(nw)
            rem(sw)
            rem(se)
        #        for i in ns:
        #            try:
        #                self.maze[i[0]][i[1]]
        #            except IndexError:
        #                ns.remove(i)
        return ns


if __name__ == '__main__':
    m = BridgedMaze()
    m.solution_print()

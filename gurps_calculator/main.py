#!/usr/bin/python3
import random
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--weapon", type=str, default=None,
                    help="set weapon power")
parser.add_argument("-a", "--armor", type=int, default=None,
                    help="set armor of target")
parser.add_argument("-z", "--antiarmor", type=float, default=None,
                    help="set weapon armor-piercing power")
parser.add_argument("-t", "--modifier", type=float, default=None,
                    help="set effectiveness of attack")
parser.add_argument("-f", "--force", "--ignore-check", action="store_true",
                    help="do not check for invalid values")
parser.add_argument("-v", "--verbose", "--debug", action="store_true",
                    help="print detailed statistics about inputted data")


def check_sane(armor, antiarmor, modifier):
    problems = []
    if float(armor) < 0:
        problems.append('Armor cannot be a detriment; armor points cannot be negative.')
    if float(antiarmor) <= 0:
        problems.append('Weapon cannot be helped by armor; antiarmor points cannot be negative or zero.')
    if float(modifier) != 0.5 and float(modifier) != 1.0 and float(modifier) != 1.5 and float(modifier) != 2.0:
        problems.append('Damage modifier is non-standard; must be in [0.5,1.0,1.5,2.0].')
    if problems:
        print('{} problem(s) in the input data:'.format(str(len(problems))))
        for i, j in enumerate(problems):
            print('\t', i + 1, ': ', j, sep='')
        print('To disable sanity checking, use the `-f` argument.')
        exit(1)


def printv(*args):
    if verbose:
        print(*args)


def printvn(*args):
    if verbose:
        print(*args, end='')


def roll_dice(num: int, sides: int, from_zero: bool = False) -> int:
    n = 0
    for i in range(num):
        printvn('\t\tDie number {} rolled '.format(i + 1))
        v = random.randint(1, sides)
        if from_zero:
            v -= 1
        printv(str(v))
        n += v
    printv('\t\tTotal: ' + str(n))
    return n


def eval_d_notation(expr: str) -> float:
    nexpr = expr.lower()
    printv('While evaluating expression `{}`, the following dice were used:'.format(expr))
    d = False
    for i in re.findall(r'\d+d\d+', nexpr):
        d = True
        printvn('\t`{}`, which means "roll '.format(i))
        if i[0] == 'd':
            i = '1' + i
        if i[-1] == 'd':
            i = i + '6'
        isp = [int(j) for j in i.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'\d+d', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'd\d+', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'd', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    if not d:
        printv('\tNo dice were used.')
    return eval(nexpr)


def formatoutput(p, a, z, t):
    printv('The received values are:')
    printv('  Power of weapon: {}'.format(p))
    printv('  Armor of target: {}'.format(a))
    printv('  Armor-piercingness of weapon: {}'.format(z))
    if float(t) > 1:
        ev = 'super effective!'
    elif float(t) < 1:
        ev = 'not very effective...'
    else:
        ev = 'nominally effective.'
    printv('  It\'s {} ({})'.format(ev, t))
    v = (eval_d_notation(p) - (float(a) / float(z))) * float(t)
    printvn('Hit ')
    print(v, end='')
    printv(' points!')
    print()


def solve(args):
    if args.weapon and args.armor and args.antiarmor and args.modifier:
        if not args.f:
            check_sane(args.armor, args.antiarmor, args.modifier)
        formatoutput(args.weapon, args.armor, args.antiarmor, args.modifier)
    else:
        P = None
        A = None
        Z = None
        T = None
        if args.weapon:
            P = args.weapon
        if args.armor:
            A = args.armor
        if args.antiarmor:
            Z = args.antiarmor
        if args.modifier:
            T = args.modifier
        interactive = ''
        if not P: interactive += 'P'
        if not A: interactive += 'A'
        if not Z: interactive += 'Z'
        if not T: interactive += 'T'
        loopnum = 0
        dictval = {'p': P, 'a': A if A else 1, 't': T if T else 1, 'z': Z if Z else 1}
        check_sane(dictval['a'], dictval['z'], dictval['t'])
        while 1:
            loopnum += 1
            dictval = {'p': P, 'a': A, 't': T, 'z': Z}
            for i in interactive:
                if verbose:
                    tmp = input('Input value of {} for evaluation number {}> '.format(i, loopnum))
                else:
                    tmp = input('{}({})?'.format(i, loopnum))
                dictval.update({i.lower(): tmp})
            if not args.force:
                check_sane(dictval['a'], dictval['z'], dictval['t'])
            formatoutput(dictval['p'], dictval['a'], dictval['z'], dictval['t'])


if __name__ == '__main__':
    args = parser.parse_args()
    verbose = args.verbose
    solve(args)

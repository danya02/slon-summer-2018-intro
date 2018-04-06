# TL;DR: 24 = (8+4) * (3-1) = (1+8-3) * 4
AKA "Easier Than it Looks".

At first, I thought that this merited a bruteforce solution, where I would place symbols randomly.
But, I thought, surely that can't be it, for you are awarded only one point for the solution.
And indeed, a much simpler method is to consider the factorization.

`24 = 2*2*2*3 = 4*6 = 2*12 = 3*8`

Noting that `12 = 8+4`, `2 = 3-1` and `6 = 8+1-3`, we can form the number in two ways:

`(8+4) * (3-1) = (1+8-3) * 4 = 24`

∎.
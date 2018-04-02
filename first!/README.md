# TL;DR: a(28) = 1028457
AKA "Python Makes This Easy".

The sequence is defined using a basic recursive loop. Specifically, it looks like this:

`a(n+1)=a(n)+a(n-1)+1`

If we were to subtract 1 from each coefficient, then it would become a standard recursive loop:

`a(n)=a(n-1)+a(n-2)+1`

And that is very easy to implement using Python, as seen [here](sequence.py). (I could've used a `lambda` function, but that would contradict PEP8.)
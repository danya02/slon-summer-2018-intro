# TL;DR: 1280
A.K.A "The `fractions` Module is Not Always Right".

The answer was found using [this script](main.py), which uses a basic bruteforce algorithm to find the answer.
Only after writing that did I figure out you [could](https://www.wolframalpha.com/input/?i=rationalize+0.30390625) [rationalize](https://www.wolframalpha.com/input/?i=rationalize+0.13984375) [these](https://www.wolframalpha.com/input/?i=rationalize+0.04453125) [numbers](https://www.wolframalpha.com/input/?i=rationalize+0.16015625) [using](https://www.wolframalpha.com/input/?i=rationalize+0.07578125) [Wolfram](https://www.wolframalpha.com/input/?i=rationalize+0.20859375) [Alpha](https://www.wolframalpha.com/input/?i=rationalize+0.0671875), then calculate the GCD of them all and arrive at the same result.
# TL;DR: [this program](main.py), input in [this file](maze.txt) (fails in most cases)
AKA "What's wrong with bridges?".

This uses the [A* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm), as  provided by [`pypaths`](https://pypi.python.org/pypi/pypaths/0.1.2).
It assigns a cost of 0 for travel with no bridge, 1 if there is a bridge, and extremely high values for impassable cells.

The problem, of course, is that it doesn't work.

That's not technically true.
It succeeds if the maze on the input is one generated by [this program](gen_maze.py), but not any valid one.
In particular, the one [given as an example](maze.txt) fails.
I haven't been able to figure out what is wrong here, so this is provided as-is.
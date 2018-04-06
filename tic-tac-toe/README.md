# TL;DR: run [this](main.py)
AKA "How about a nice game of **Global Thermonuclear War**?"

The program has a object-based structure, where each player is an object, both are managed by the board, which queries players for their `next_move()`.
AI players are implemented as a subclass of players.

There are 3 AI opponents implemented.
`RandomAI` selects moves at random.
`SequentialStrategyAI` tries verticals, then horizontals and then diagonals to find a solution.
`CornerSeekerAI` tries corners, then center, then sides, and is a ripoff of an algorithm from [here](https://inventwithpython.com/chapter10.html).

The GUI is a subclass of `Player`, delays while the player is selecting a move, runs a nice drawing animation whenever it detects that the board has been updated, but is otherwise absolute shite.
If this will become a popular thing (hint: won't happen), then the architecture should be rebuilt.
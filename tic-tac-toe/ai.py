#!/usr/bin/python3
import player
import board
import random
import copy


class AI(player.Player):
    def __init__(self, board: board.TicTacToeBoard):
        super().__init__(board)
        self.description = 'Superclass for all AI opponents. Unplayable.'

    def is_dead(self):
        return self.__class__.__name__=='AI'


class RandomAI(AI):
    def __init__(self, board: board.TicTacToeBoard):
        super().__init__(board)
        self.description = 'Stateless. Selects its moves entirely randomly.'

    def next_move(self):
        return random.randint(0, 2), random.randint(0, 2)


class SequentialStrategyAI(AI):
    def __init__(self, board: board.TicTacToeBoard):
        super().__init__(board)
        self.strategy = 0
        self.pos = 0
        self.subpos = 0
        self.dead = False
        self.description = 'Stateful. Tries verticals, then horizontals, ' \
                           'then diagonals, then dies. '

    def is_dead(self):
        return self.dead

    def reset_state(self):
        self.strategy = 0
        self.pos = 0
        self.subpos = 0
        self.dead = False

    def tell_bad_move(self):
        self.subpos += 1
        if self.subpos > 2:
            self.pos += 1
            self.subpos = 0
            if self.pos > (2 if self.strategy != 2 else 1):
                self.pos = 0
                self.strategy += 1
                if self.strategy > 2:
                    self.dead = True

    def next_move(self):
        if self.strategy == 0:
            move = (self.pos, self.subpos)
        elif self.strategy == 1:
            move = (self.subpos, self.pos)
        else:
            if self.pos == 0:
                move = (self.subpos, self.subpos)
            else:
                move = (self.subpos, 2 - self.subpos)
        return move


class CornerSeekerAI(AI):
    def __init__(self, gameboard: board.TicTacToeBoard):
        super().__init__(gameboard)
        self.description = 'Stateless. Seeks to cover corners, then center, then sides. Shamelessly ripped off from ' \
                           'https://inventwithpython.com/chapter10.html'
        self.board_clone = board.TicTacToeBoard()
        self.player_num = 2
        self.opponent_num = 1
        self.dead = False

    def is_dead(self):
        return self.dead

    def next_move(self):
        # Step 1: test for my win in one move
        for x in range(3):
            for y in range(3):
                self.board_clone.board = copy.deepcopy(self.board.board)
                if self.board_clone.board[x][y] == 0:
                    self.board_clone.board[x][y] = self.player_num
                    if self.board_clone.check_win() == self.player_num:
                        return x, y
        # Step 2: test for my loss in one move
        for x in range(3):
            for y in range(3):
                self.board_clone.board = copy.deepcopy(self.board.board)
                if self.board_clone.board[x][y] == 0:
                    self.board_clone.board[x][y] = self.opponent_num
                    if self.board_clone.check_win() == self.opponent_num:
                        return x, y
        # Step 3: try corners
        for i in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            if self.board.board[i[0]][i[1]] == 0:
                return i
        # Step 4: try center
        if self.board.board[1][1] == 0:
            return 1, 1

        # Step 5: try sides
        for i in [(1, 0), (0, 1), (2, 1), (1, 2)]:
            if self.board.board[i[0]][i[1]] == 0:
                return i
        # Step 6: if nothing successful, we give up
        self.dead = True
        return 0, 0

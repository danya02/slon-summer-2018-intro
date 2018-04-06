#!/usr/bin/python3
import player


class TicTacToeBoard:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player1 = player.Player(self)
        self.player2 = player.Player(self)

    def reset_board(self) -> None:
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def check_valid_move(self, move: (int, int)) -> bool:
        return self.board[move[0]][move[1]] == 0

    def check_win(self) -> int:
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[1][1]
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    return 0
        return -1

    def apply_move(self, player: int, move: (int, int)):
        self.board[move[0]][move[1]] = player

    def play_round(self) -> None:
        self.reset_board()
        while not self.check_win():
            if self.player1.is_dead():
                raise UserWarning('Player 1 is dead!')
            if self.player2.is_dead():
                raise UserWarning('Player 2 is dead!')
            m = self.player1.next_move()
            while not self.check_valid_move(m):
                if self.player1.is_dead():
                    raise UserWarning('Player 1 is dead!')
                if self.player2.is_dead():
                    raise UserWarning('Player 2 is dead!')
                self.player1.tell_bad_move()
                m = self.player1.next_move()
            self.apply_move(1, m)

            if self.check_win():
                break
            if self.player1.is_dead():
                raise UserWarning('Player 1 is dead!')
            if self.player2.is_dead():
                raise UserWarning('Player 2 is dead!')
            m = self.player2.next_move()
            while not self.check_valid_move(m):
                if self.player1.is_dead():
                    raise UserWarning('Player 1 is dead!')
                if self.player2.is_dead():
                    raise UserWarning('Player 2 is dead!')
                self.player2.tell_bad_move()
                m = self.player2.next_move()
            self.apply_move(2, m)
        if self.check_win() == 1:
            self.player1.tell_win()
            self.player2.tell_lose()
        elif self.check_win() == 2:
            self.player1.tell_lose()
            self.player2.tell_win()
        else:
            self.player1.tell_draw()
            self.player2.tell_draw()
        self.player1.reset_state()
        self.player2.reset_state()

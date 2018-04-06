#!/usr/bin/python3
import board


class Player:
    def __init__(self, board: board.TicTacToeBoard):
        self.board = board

    def next_move(self) -> (int, int):
        return 0, 0

    def is_dead(self) -> bool:
        return False

    def tell_bad_move(self) -> None:
        pass

    def tell_win(self) -> None:
        pass

    def tell_lose(self) -> None:
        pass

    def tell_draw(self) -> None:
        pass

    def reset_state(self) -> None:
        pass

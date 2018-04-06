#!/usr/bin/python3
import os
import pygame
import threading
import math
import inspect

import ai
import player
import board


class GUI(player.Player):
    def __init__(self, opponentclass):
        boardinst = board.TicTacToeBoard()
        super().__init__(boardinst)
        self.board.player1 = self
        self.board.player2 = opponentclass(self.board)
        pygame.init()
        self.display = pygame.display.set_mode((300, 300))
        self.move = None
        self.win = False
        self.lose = False
        self.draw = False
        self.update_board = False
        self.dead = False
        self.other_dead = False
        self.since_update = 0
        self.last_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.clock = pygame.time.Clock()
        self.draw_thread = threading.Thread(target=self.draw_loop, name='draw loop')
        self.draw_thread.start()
        while not self.dead:
            try:
                self.board.play_round()
            except UserWarning:
                self.other_dead = True
            pygame.time.delay(5000)

    def is_dead(self):
        return self.dead

    def next_move(self):
        self.update_board = True
        while self.move is None:
            pass
        move = self.move
        self.move = None
        return move

    def tell_win(self):
        self.since_update = 0
        self.win = True

    def tell_lose(self):
        self.since_update = 0
        self.lose = True

    def tell_draw(self):
        self.since_update = 0
        self.draw = True

    @staticmethod
    def delinearize(pos: int) -> (int, int):
        return divmod(pos, 3)

    @staticmethod
    def linearize(pos: (int, int)) -> int:
        return pos[1] + 3 * pos[0]

    def update_last_board(self):
        for x in range(3):
            for y in range(3):
                self.last_board[x][y] = self.board.board[x][y]

    def draw_loop(self):
        rects = [pygame.Rect(0, 0, 100, 100) for i in range(9)]
        for i in range(3):
            rects[i * 3].centerx = 50
            rects[i * 3 + 1].centerx = 150
            rects[i * 3 + 2].centerx = 250
        for i in range(3):
            rects[i].centery = 50
            rects[i + 3].centery = 150
            rects[i + 6].centery = 250
        keymap = {pygame.K_1: (2, 0), pygame.K_2: (2, 1), pygame.K_3: (2, 2), pygame.K_4: (1, 0), pygame.K_5: (1, 1),
                  pygame.K_6: (1, 2), pygame.K_7: (0, 0), pygame.K_8: (0, 1), pygame.K_9: (0, 2), pygame.K_KP1: (2, 0),
                  pygame.K_KP2: (2, 1), pygame.K_KP3: (2, 2), pygame.K_KP4: (1, 0), pygame.K_KP5: (1, 1),
                  pygame.K_KP6: (1, 2), pygame.K_KP7: (0, 0), pygame.K_KP8: (0, 1), pygame.K_KP9: (0, 2)
                  }
        f = pygame.font.SysFont('BuiltIn', 32)
        fl = pygame.font.SysFont('BuiltIn', 64)
        while 1:
            self.since_update += 1
            self.display.fill(pygame.Color('black'))
            for i in rects:
                pygame.draw.rect(self.display, pygame.Color('white'), i, 1)
            for x in range(3):
                for y in range(3):
                    if self.last_board[x][y] == 1:
                        r = rects[self.linearize((x, y))]
                        pygame.draw.line(self.display, pygame.Color('red'), r.topleft, r.bottomright, 5)
                        pygame.draw.line(self.display, pygame.Color('red'), r.topright, r.bottomleft, 5)
                    elif self.last_board[x][y] == 2:
                        pygame.draw.arc(self.display, pygame.Color('blue'), rects[self.linearize((x, y))],
                                        0, 2 * math.pi, 5)
                    else:
                        t = f.render(str(7 + y - (3 * x)), True, pygame.Color('white'))
                        r = rects[self.linearize((x, y))]
                        self.display.blit(t, (r.right - t.get_width(), r.bottom - t.get_height()))
            if self.last_board != self.board.board:
                self.since_update = 0
                self.update_board = False
                for x in range(3):
                    for y in range(3):
                        if self.last_board[x][y] != self.board.board[x][y]:
                            if self.board.board[x][y] == 1:
                                r = rects[self.linearize((x, y))]
                                for i in range(50):
                                    pygame.draw.line(self.display, pygame.Color('red'), r.topleft,
                                                     (r.left + (i * 2), r.top + (i * 2)), 5)
                                    pygame.display.flip()
                                    self.clock.tick(200)
                                for i in range(50):
                                    pygame.draw.line(self.display, pygame.Color('red'), r.topleft, r.bottomright, 5)
                                    pygame.draw.line(self.display, pygame.Color('red'), r.topright,
                                                     (r.right - (i * 2), r.top + (i * 2)), 5)
                                    pygame.display.flip()
                                    self.clock.tick(200)
                for x in range(3):
                    for y in range(3):
                        if self.board.board[x][y] == 2:
                            for i in range(90):
                                pygame.draw.arc(self.display, pygame.Color('blue'), rects[self.linearize((x, y))],
                                                0, 2 * math.pi * (4 / 360) * i, 5)
                                pygame.display.flip()
                                self.clock.tick(200)

            if self.win:
                self.win = False
                self.board.reset_board()
                s = self.display.copy()
                t = fl.render('Player1 WIN', True, pygame.Color('red'))
                tr = t.get_rect()
                sr = s.get_rect()
                for i in range(255):
                    tr.centerx = sr.centerx
                    tr.centery = i
                    self.display.blit(s, (0, 0))
                    self.display.blit(t, tr)
                    self.display.fill(pygame.Color(i, i, i, 255), special_flags=pygame.BLEND_ADD)
                    pygame.display.flip()
                    self.clock.tick(60)
            if self.lose:
                self.lose = False
                self.board.reset_board()
                s = self.display.copy()
                t = fl.render('Player2 WIN', True, pygame.Color('blue'))
                tr = t.get_rect()
                sr = s.get_rect()
                for i in range(255):
                    tr.centerx = sr.centerx
                    tr.centery = i
                    self.display.blit(s, (0, 0))
                    self.display.blit(t, tr)
                    self.display.fill(pygame.Color(i, i, i, 255), special_flags=pygame.BLEND_ADD)
                    pygame.display.flip()
                    self.clock.tick(60)
            if self.draw:
                self.draw = False
                self.board.reset_board()
                s = self.display.copy()
                t = fl.render('DRAW', True, pygame.Color('yellow'))
                tr = t.get_rect()
                sr = s.get_rect()
                for i in range(255):
                    tr.centerx = sr.centerx
                    tr.centery = i
                    self.display.blit(s, (0, 0))
                    self.display.blit(t, tr)
                    self.display.fill(pygame.Color(i, i, i, 255), special_flags=pygame.BLEND_ADD)
                    pygame.display.flip()
                    self.clock.tick(60)
            if self.other_dead:
                s = self.display.copy()
                t = fl.render('Player2 DEAD', True, pygame.Color('red'))
                tr = t.get_rect()
                sr = s.get_rect()
                for i in range(255):
                    tr.centerx = sr.centerx
                    tr.centery = i
                    self.display.blit(s, (0, 0))
                    self.display.blit(t, tr)
                    self.display.fill(pygame.Color(i, i, i, 255), special_flags=pygame.BLEND_ADD)
                    pygame.display.flip()
                    self.clock.tick(60)
                os.abort()
            self.update_last_board()
            pygame.display.flip()
            self.clock.tick(10)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.dead = True
                    exit(0)
                if i.type == pygame.KEYDOWN:
                    if i.key in [pygame.K_q, pygame.K_ESCAPE]:
                        self.dead = True
                        exit(0)
                    if i.key in keymap:
                        self.move = keymap[i.key]

                if i.type == pygame.MOUSEBUTTONDOWN:
                    for j in rects:
                        if j.collidepoint(i.pos[0], i.pos[1]):
                            self.move = self.delinearize(rects.index(j))


class AISelector:
    def __init__(self):
        pygame.init()
        self.display = None
        self.run = True
        self.opponent = None
        self.cursor = (0, 0)
        self.click = None

        self.thread = threading.Thread(target=self.drawloop, name='AISelector drawloop')
        self.thread.start()

    def drawloop(self):
        ai_list = []
        for name, obj in inspect.getmembers(ai):
            if inspect.isclass(obj):
                ai_list.append(tuple([name, obj]))
        ai_labels = []
        false_board = board.TicTacToeBoard()
        for i in ai_list:
            a = i[1](false_board)
            ai_labels += [(i[0], a.description, i[1])]
            del a
        fb = pygame.font.SysFont("BuiltIn", 32)
        fs = pygame.font.SysFont("BuiltIn", 24)
        ai_surfaces = []
        for i in ai_labels:
            tb = fb.render(i[0], True, pygame.Color('white'))
            ts = fs.render(i[1], True, pygame.Color('white'))
            ai_surfaces += [(tb, ts, i[2])]
        height = fb.get_height() * len(ai_surfaces)
        width = 0
        for i in ai_surfaces:
            width = max(width, i[0].get_width() + i[1].get_width())
        self.display = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        while not self.opponent:
            self.display.fill(pygame.Color('black'))
            for i, j in enumerate(ai_surfaces):
                j0r = j[0].get_rect()
                j0r.topleft = (0, fb.get_height() * i)
                self.display.blit(j[0], j0r)
                j1r = j[1].get_rect()
                j1r.topleft = (j[0].get_width(), fb.get_height() * i)
                self.display.blit(j[1], j1r)
                pygame.draw.rect(self.display, pygame.Color('white') if not (
                            j0r.collidepoint(*self.cursor) or j1r.collidepoint(*self.cursor)) else pygame.Color('red'),
                                 j0r, 1)
                pygame.draw.rect(self.display, pygame.Color('white') if not (
                            j0r.collidepoint(*self.cursor) or j1r.collidepoint(*self.cursor)) else pygame.Color('red'),
                                 j1r, 1)
                if self.click is not None:
                    if j0r.collidepoint(*self.click) or j1r.collidepoint(*self.click):
                        self.opponent = j[2]
                        return None
            pygame.display.flip()
            clock.tick(30)
            for i in pygame.event.get():
                if i.type == pygame.MOUSEMOTION:
                    self.cursor = i.pos
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    self.click = i.pos


if __name__ == '__main__':
    a = AISelector()
    while not a.opponent:
        pass
    print(a.opponent)
    g = GUI(a.opponent)

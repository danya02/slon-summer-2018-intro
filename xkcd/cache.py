#!/usr/bin/python3
import json
import logging as l
import os
import random
import threading
import time
import math
import urllib.error
import urllib.request

display = None
try:
    import pygame

    pygame.init()
    display = pygame.display.set_mode((100, 100))
    NOGUI = False
except ImportError:
    l.warning("Error while importing pygame; no GUI will be displayed.")
    NOGUI = True
except pygame.error:
    l.warning("Error while initializing display; no GUI will be displayed.")
    NOGUI = True

maxnum = 1


class DisplayManager(threading.Thread):
    def __init__(self):
        super().__init__()
        self.spinner_phase_1 = 0.0
        self.spinner_phase_2 = 3.141
        self.spinner_color = pygame.Color('white')
        self.display = pygame.display.set_mode((800, 600))
        self.daemon = True
        self.image = pygame.Surface((0, 0))
        self.image_to_blit = None
        self.clock = pygame.time.Clock()
        self.num = 0
        self.max = 1
        self.start()

    def run(self):
        while 1:
            self.image_to_blit = self.image.convert()
            self.image_to_blit.fill(pygame.Color(192, 192, 192, 100), special_flags=pygame.BLEND_MIN)
            self.display.fill(pygame.Color('black'))
            self.display.blit(self.image_to_blit, (
            400 - (self.image_to_blit.get_width() // 2), 300 - (self.image_to_blit.get_height() // 2)))
            r = pygame.Rect(0, 0, 100, 100)
            r.center = self.display.get_rect().center
            pygame.draw.arc(self.display, self.spinner_color, r, self.spinner_phase_1, self.spinner_phase_2, 10)
            self.spinner_phase_1 += 0.1
            self.spinner_phase_2 = self.spinner_phase_1 + abs(
                math.sin(time.time()) * math.pi * max(self.num / self.max, 0.1))
            pygame.display.flip()
            self.clock.tick(30)

    def set_error(self) -> None:
        self.spinner_color = pygame.Color('red')

    def unset_error(self) -> None:
        self.gen_color()

    def gen_color(self):
        self.spinner_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def set_val(self, n: int):
        self.num = n
        self.image = pygame.image.load('{}/img.png'.format(str(n)))


dm = None
if not NOGUI:
    dm = DisplayManager()


def download_json(url: str) -> dict:
    if not NOGUI:
        dm.unset_error()
        dm.gen_color()
    l.debug("Downloading JSON from {}...".format(url))
    r = b''
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            r = response.read()
    except urllib.error.URLError:
        l.error("Timeout while trying to connect to {}!".format(url))
    try:
        r = r.decode('utf-8')
        r = json.loads(r)
    except UnicodeDecodeError:
        l.error("Data received isn't UTF-8 encoded!")
        if not NOGUI:
            dm.set_error()
    except json.decoder.JSONDecodeError:
        l.error("Data received isn't JSON!")
        if not NOGUI:
            dm.set_error()
    if not isinstance(r, dict):
        raise ValueError
    return r


def download(url: str, save_to: str) -> None:  # idea swiped from https://stackoverflow.com/a/7244263
    if not NOGUI:
        dm.unset_error()
        dm.gen_color()
    l.debug("Downloading file from {} to {}".format(url, save_to))
    try:
        with urllib.request.urlopen(url, timeout=10) as response, open(save_to, 'wb') as out_file:
            data = response.read(1)
            while not data == b'':
                out_file.write(data)
                data = response.read(1)
    except urllib.error.URLError:
        l.error("Timeout while trying to connect to {}!".format(url))
        if not NOGUI:
            dm.set_error()


def get_comic(n: int) -> None:
    obj = download_json('http://xkcd.com/{}/info.0.json'.format(str(n)))
    try:
        os.mkdir(str(n))
    except FileExistsError:
        pass
    os.chdir(str(n))
    with open('info.json', 'w') as o:
        json.dump(obj, o)
    download(obj['img'], 'img.png')
    os.chdir('..')
    print('Downloaded {}/{} ({}% done): {}   '.format(str(n), str(maxnum), str(n/maxnum*100), obj['safe_title']))
    if not NOGUI:
        pygame.display.set_caption(str(obj['num']) + ': ' + obj['safe_title'])
        dm.set_val(n)


def download_all() -> None:
    obj = download_json('https://xkcd.com/info.0.json')
    global maxnum
    maxnum = obj['num']
    if not NOGUI:
        dm.max = obj['num']
    for i in range(1, obj['num']):
        get_comic(i)


if __name__ == '__main__':
    download_all()

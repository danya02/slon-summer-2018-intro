#!/ust/bin/python3
import logging as l

l.root.setLevel(l.DEBUG)
import urllib.request, urllib.error
import os
import json
import random
import threading

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


class DisplayManager(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.spinner = False
        self.spinner_phase = 0
        self.spinner_color = pygame.Color('white')
        self.display = pygame.display.get_surface()
        self.image = pygame.Surface((100, 100))
        self.image_to_blit = self.image.copy()
        self.last_size = self.image.get_size()
        self.clock = pygame.time.Clock()
        self.request_lock = False
        self.error = False
        self.start()

    def run(self) -> None:
        while 1:
            if self.image.get_size() != self.last_size:
                self.display = pygame.display.set_mode(self.image.get_size())
            self.last_size = self.image.get_size()
            self.image_to_blit = self.image.convert()
            if self.spinner:
                self.image_to_blit.fill(pygame.Color(192, 192, 192, 100), special_flags=pygame.BLEND_MIN)
                midx = self.image_to_blit.get_width() // 2
                midy = self.image_to_blit.get_height() // 2
                rect_size = 10
                roff = rect_size * 2
                rects = [pygame.Rect(0, 0, rect_size, rect_size) for _ in range(8)]
                rects[0].center = (midx - roff, midy - roff)
                rects[1].center = (midx, midy - roff)
                rects[2].center = (midx + roff, midy - roff)
                rects[3].center = (midx + roff, midy)
                rects[4].center = (midx + roff, midy + roff)
                rects[5].center = (midx, midy + roff)
                rects[6].center = (midx - roff, midy + roff)
                rects[7].center = (midx - roff, midy)

                for i, j in enumerate(rects):
                    if i != self.spinner_phase:
                        self.image_to_blit.fill(self.spinner_color, j)
                self.spinner_phase += 1
                if self.spinner_phase >= 8:
                    self.spinner_phase = 0
            if self.error:
                font = pygame.font.SysFont('Arial', 16, False, False)
                self.image_to_blit.blit(
                    font.render('Error while downloading!', True, pygame.Color('red'), pygame.Color(0, 0, 0, 127)),
                    (self.image_to_blit.get_width() // 3, self.image_to_blit.get_height() // 2))
            self.display.blit(self.image_to_blit, (0, 0))
            pygame.display.flip()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    os.abort()
                elif i.type == pygame.MOUSEBUTTONDOWN and not self.request_lock:
                    self.request_lock = True
                    t = threading.Thread(target=display_comic, args=(get_random_comic_num,))
                    t.start()
            self.clock.tick(10)

    def set_image(self, image: pygame.Surface) -> None:
        self.image = image

    def set_spinner(self, color: pygame.Color = pygame.Color('red')) -> None:
        self.spinner = True
        self.spinner_color = color
        self.spinner_phase = 0

    def unset_spinner(self) -> None:
        self.spinner = False

    def set_error(self) -> None:
        self.error = True

    def unset_error(self) -> None:
        self.error = False

    def set_title(self, title: str) -> None:
        pygame.display.set_caption(title)


dm = None
if not NOGUI:
    dm = DisplayManager()


def download(url: str, save_to: str) -> None:  # idea swiped from https://stackoverflow.com/a/7244263
    if not NOGUI:
        dm.unset_error()
        dm.set_spinner(pygame.Color('blue'))
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
    if not NOGUI:
        dm.unset_spinner()


def download_json(url: str, green_spin: bool = False) -> dict:
    if not NOGUI:
        dm.unset_error()
        dm.set_spinner(pygame.Color('yellow' if not green_spin else 'green'))
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
    if not NOGUI:
        dm.unset_spinner()
    if not isinstance(r, dict):
        raise ValueError
    return r


def get_comic(n: int) -> str:
    if os.path.exists(str(n)) and os.path.isdir(str(n)):
        return str(n) + os.path.sep + 'img.png'
    else:
        obj = download_json('http://xkcd.com/{}/info.0.json'.format(str(n)))
        os.mkdir(str(n))
        os.chdir(str(n))
        with open('info.json', 'w') as o:
            json.dump(obj, o)
        download(obj['img'], 'img.png')
        os.chdir('..')
        return str(n) + os.path.sep + 'img.png'


def display_comic(n: int) -> None:
    if callable(n):
        n = n()
    path = get_comic(n)
    info = json.load(open('{}/info.json'.format(str(n))))
    if not NOGUI:
        dm.request_lock = False
        comic = pygame.image.load(path)
        dm.set_image(comic)
        dm.set_title('{}: {}'.format(str(n), info['safe_title']))
        print('Released on {}-{}-{}'.format(info['year'], info['month'], info['day']))
        print('Title text:')
        print(info['alt'] if info['alt'] != '' else '<<Title text empty>>')
    else:
        l.info('GUI initialization failed; printing title and transcript to stdout.')
        print('{}: {}'.format(str(n), info['safe_title']))
        print('~' * len('{}: {}'.format(str(n), info['safe_title'])))
        print('Released on {}-{}-{}'.format(info['year'], info['month'], info['day']))
        print()
        print('Transcript:')
        print(info['transcript'] if info['transcript'] != '' else '<<Transcript empty>>')
        print()
        print('Title text:')
        print(info['alt'] if info['alt'] != '' else '<<Title text empty>>')


def get_random_comic_num() -> int:
    obj = download_json('https://xkcd.com/info.0.json', True)
    return random.randint(1, obj['num'])


if __name__ == '__main__':
    while 1:
        display_comic(get_random_comic_num())
        input('Press <ENTER> for next comic> ')

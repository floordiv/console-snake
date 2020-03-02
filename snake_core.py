import select
import sys
import termios
import tty
import os
from random import randint


def getch(timeout=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)


class data:
    xres = 50
    yres = 20

    speed = 0.05

    content = []
    max_snake_len = 1
    snake_body_pos = [[xres // 2, yres // 2]]
    snake_body = ['-']
    food_pos = []
    food_model = '*'
    vector = {
        'x_move': '─',
        'y_move': '│'
    }
    angles = {
        'down-right': '└',
        'down-left': '┘',
        'up-right': '┌',
        'up-left': '┐',
    }

    @staticmethod
    def check_move(coords):
        return 'y_move' if coords[0] == 0 else 'x_move'


class screen:
    @staticmethod
    def clear():
        os.system('clear')

    @staticmethod
    def text(text):
        text_xminus = len(text) // 2
        text_xplus = len(text) - text_xminus
        data.content[data.yres // 2][data.xres // 2 - text_xminus:data.xres // 2 + text_xplus] = list(text)
        screen.draw()
        input()
        sys.exit()

    @staticmethod
    def draw(top_text=False, print_score=True):
        screen.clear()
        if top_text:
            print(top_text)
        if print_score:
            print('\n\nScore:', data.max_snake_len)
        print('=' * (data.xres + 2))
        for each in data.content:
            print('|' + ''.join(each) + '|')
        print('=' * (data.xres + 2))

    @staticmethod
    def init():
        for index in range(data.yres):
            data.content.append(list(' ' * data.xres))


def move_snake(coords):
    new_coords = [data.snake_body_pos[-1][0] + coords[0], data.snake_body_pos[-1][1] + coords[1]]
    if new_coords == data.food_pos:
        data.max_snake_len += 1
        data.food_pos = []
    if new_coords[0] >= data.xres or new_coords[0] < 0 or new_coords[1] >= data.yres or new_coords[1] < 0:
        screen.text('GAME OVER. PRESS ENTER TO CONTINUE')
    if new_coords in data.snake_body_pos and len(data.snake_body_pos) > 2:
        screen.text('GAME OVER. PRESS ENTER TO CONTINUE')
    data.snake_body_pos.append(new_coords)
    data.snake_body.append(data.vector[data.check_move(coords)])
    for index, each in enumerate(data.snake_body_pos):
        data.content[each[1]][each[0]] = ' '
    if len(data.snake_body_pos) > data.max_snake_len:
        del data.snake_body_pos[0]
        del data.snake_body[0]
    for index, each in enumerate(data.snake_body_pos):
        data.content[each[1]][each[0]] = data.snake_body[index]


def spawn_food():
    if len(data.food_pos) == 0:
        food_pos = [randint(0, data.xres - 1), randint(0, data.yres - 1)]
        while food_pos in data.snake_body_pos:      # to avoid spawning food inside snake's body
            food_pos = [randint(0, data.xres), randint(0, data.yres)]
        data.content[food_pos[1]][food_pos[0]] = data.food_model
        data.food_pos = food_pos


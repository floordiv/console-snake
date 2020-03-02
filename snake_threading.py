import snake_core as core
from threading import Thread
from time import sleep
from sys import exit
from traceback import format_exc


core.screen.init()


class data:
    binds = {
        'w': [0, -1],
        's': [0, 1],
        'a': [-1, 0],
        'd': [1, 0]
    }
    prev_key = 'q'
    reversed_keys = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w', 'q': 't'}
    key = 'd'


def key_press():
    while True:
        core.spawn_food()
        key = core.getch()
        if key == 'f':
            exit()
        if key == data.reversed_keys[data.prev_key] and len(core.data.snake_body) < 2:
            continue
        if key in data.binds:
            data.prev_key = key


def move():
    while True:
        sleep(core.data.speed)

        core.move_snake(data.binds[data.key])
        core.screen.draw()


Thread(target=key_press).start()
Thread(target=move).start()

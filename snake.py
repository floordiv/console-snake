import snake_core as core
from time import sleep
from sys import exit


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


while True:
    core.spawn_food()
    sleep(core.data.speed)
    key = core.getch()
    if key == 'f':
        exit()
    if key == data.reversed_keys[data.prev_key]:
        continue
    if key in data.binds:
        data.prev_key = key
        core.move_snake(data.binds[key])
        core.screen.draw()


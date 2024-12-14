from dataclasses import dataclass
from itertools import product
import re
import os
os.chdir(os.path.dirname(__file__))

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Vector:
    x: int
    y: int

@dataclass
class Machine:
    button_a: Vector
    button_b: Vector
    prize: Point

MAX_PRESSES = 100
COST_A = 3
COST_B = 1

def main():
    machines: list[Machine] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = iter(f.readlines())
    while True:
        try:
            match_a = re.match(r'.*X\+(?P<x>\d+), Y\+(?P<y>\d+)', next(lines))
            match_b = re.match(r'.*X\+(?P<x>\d+), Y\+(?P<y>\d+)', next(lines))
            match_prize = re.match(r'.*X=(?P<x>\d+), Y=(?P<y>\d+)', next(lines))

            button_a = Vector(int(match_a['x']), int(match_a['y']))
            button_b = Vector(int(match_b['x']), int(match_b['y']))
            prize = Point(int(match_prize['x']), int(match_prize['y']))
            machines.append(Machine(button_a, button_b, prize))

            next(lines)
        except StopIteration:
            break

    total_tokens = 0
    for m in machines:
        min_cost = -1
        for a_presses, b_presses in product(range(0, MAX_PRESSES + 1), range(0, MAX_PRESSES + 1)):
            x = a_presses * m.button_a.x + b_presses * m.button_b.x
            y = a_presses * m.button_a.y + b_presses * m.button_b.y
            if m.prize.x == x and m.prize.y == y:
                cost = a_presses * COST_A + b_presses * COST_B
                if min_cost == -1 or cost < min_cost:
                    min_cost = cost
        if min_cost != -1:
            total_tokens += min_cost

    print(f'Total tokens spent: {total_tokens}')

if __name__ == '__main__':
    main()

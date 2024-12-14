from dataclasses import dataclass
import re
import os
from sympy import Eq, solve
from sympy.abc import a, b
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
PART2 = True

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

    if PART2:
        for m in machines:
            m.prize.x += 10000000000000
            m.prize.y += 10000000000000

    total_tokens = 0
    for m in machines:
        eq_x = Eq(m.prize.x, a * m.button_a.x + b * m.button_b.x)
        eq_y = Eq(m.prize.y, a * m.button_a.y + b * m.button_b.y)
        result = solve((eq_x, eq_y), (a, b))
        if result[a] == int(result[a]) and result[b] == int(result[b]):
            total_tokens += result[a] * COST_A + result[b] * COST_B

    print(f'Total tokens spent: {total_tokens}')

if __name__ == '__main__':
    main()

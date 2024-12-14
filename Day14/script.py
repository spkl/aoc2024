from dataclasses import dataclass, field
from math import prod
import re
import os
import png
os.chdir(os.path.dirname(__file__))

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Velocity:
    x: int
    y: int

@dataclass
class Robot:
    point: Point
    velocity: Velocity
    origin: Point|None = None

    def init(self):
        self.origin = Point(self.point.x, self.point.y)

    def reset(self):
        self.point = Point(self.origin.x, self.origin.y)

    def move(self):
        nx, ny = self.point.x + self.velocity.x, self.point.y + self.velocity.y
        self.point = Point(nx, ny)

    def normalize(self, width, height):
        self.point = Point(self.point.x % width, self.point.y % height)

    def is_in_quadrant(self, quadrant: 'Quadrant') -> bool:
        return quadrant.min.x <= self.point.x <= quadrant.max.x \
            and quadrant.min.y <= self.point.y <= quadrant.max.y

@dataclass
class Quadrant:
    min: Point
    max: Point
    robots: list[Robot] = field(default_factory=lambda: [])

def main():
    robots: list[Robot] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = iter(f.readlines())
        width, height = next(lines).strip().split('x')
        width, height = int(width), int(height)
        for line in lines:
            m = re.match(r'p=(?P<px>\d+),(?P<py>\d+) v=(?P<vx>\-?\d+),(?P<vy>\-?\d+)', line)
            px, py, vx, vy = int(m['px']), int(m['py']), int(m['vx']), int(m['vy'])
            r = Robot(Point(px, py), Velocity(vx, vy))
            r.init()
            robots.append(r)

    seconds = 100
    for _ in range(seconds):
        for r in robots:
            r.move()

    for r in robots:
        r.normalize(width, height)

    q1 = Quadrant(Point(0, 0), Point(width // 2 - 1, height // 2 - 1))
    q2 = Quadrant(Point(width // 2 + 1, 0), Point(width - 1, height // 2 - 1))
    q3 = Quadrant(Point(0, height // 2 + 1), Point(width // 2 - 1, height - 1))
    q4 = Quadrant(Point(width // 2 + 1, height // 2 + 1), Point(width - 1, height - 1))
    quadrants = [q1, q2, q3, q4]
    for r in robots:
        for q in quadrants:
            if r.is_in_quadrant(q):
                q.robots.append(r)

    safety_factor = prod(len(q.robots) for q in quadrants)
    print(f'Safety factor: {safety_factor}')

    for r in robots:
        r.reset()

    for frame in range(1, 10000):
        for r in robots:
            r.move()
            r.normalize(width, height)
        img = [[0 for _ in range(width)] for _ in range(height)]
        for r in robots:
            img[r.point.y][r.point.x] = 255
        # Only save images that have at least 20 robots in one line
        if any(line for line in img if sum(line) > 255 * 20):
            png.from_array(img, 'L').save(f'frames/{frame}.png')

if __name__ == '__main__':
    main()

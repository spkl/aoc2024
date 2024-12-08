import os
from collections import namedtuple
from itertools import product, count
os.chdir(os.path.dirname(__file__))

Point = namedtuple('Point', ['x', 'y'])

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        area = [line.strip() for line in f.readlines()]
    min_x, min_y = 0, 0
    max_x, max_y = len(area[0]) - 1, len(area) - 1

    antennas: dict[str, list[Point]] = {}
    antinodes: set[Point] = set()
    antinodes2: set[Point] = set()
    for y, line in enumerate(area):
        for x, char in enumerate(line):
            if char == '.':
                continue
            points = antennas.setdefault(char, [])
            points.append(Point(x, y))

    for points in antennas.values():
        for src, dst in product(points, repeat=2):
            if src == dst:
                continue
            x = (dst.x - src.x) * 2 + src.x
            y = (dst.y - src.y) * 2 + src.y
            if x < min_x or x > max_x or y < min_y or y > max_y:
                continue
            antinodes.add(Point(x, y))

    for points in antennas.values():
        for src, dst in product(points, repeat=2):
            if src == dst:
                continue
            antinodes2.add(src)
            antinodes2.add(dst)
            diff_x = dst.x - src.x
            diff_y = dst.y - src.y
            for m in count(2):
                x = diff_x * m + src.x
                y = diff_y * m + src.y
                if x < min_x or x > max_x or y < min_y or y > max_y:
                    break
                antinodes2.add(Point(x, y))


    print(f'Antinodes: {len(antinodes)}')
    print(f'Antinodes2: {len(antinodes2)}')

if __name__ == '__main__':
    main()

import os
from collections import namedtuple
os.chdir(os.path.dirname(__file__))

Point = namedtuple('Point', ['x', 'y'])
DirectedPoint = namedtuple('DirectedPoint', ['point', 'direction'])
vectors = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}
turns = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}

def is_in_area(area: list[str], pos: Point) -> bool:
    return pos.x >= 0 and pos.x < len(area[0]) and pos.y >= 0 and pos.y < len(area)

def walk(area: list[str], pos: Point, direction: str) -> tuple[int, set[Point]]:
    visited: set[Point] = set()
    visited_with_direction: set[DirectedPoint] = set()
    while True:
        visited.add(pos)
        directed_pos = DirectedPoint(pos, direction)
        if directed_pos in visited_with_direction:
            return -1, visited
        visited_with_direction.add(directed_pos)

        vector = vectors[direction]
        next_pos = Point(pos.x + vector[0], pos.y + vector[1])
        if not is_in_area(area, next_pos):
            break
        if area[next_pos.y][next_pos.x] == '#':
            direction = turns[direction]
        else:
            pos = next_pos
    return len(visited), visited

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        area = [line.strip() for line in f.readlines()]

    pos: Point|None = None
    direction: str = None
    for y, line in enumerate(area):
        for x, char in enumerate(line):
            if char not in ('.', '#'):
                pos = Point(x, y)
                direction = area[pos.y][pos.x]
    assert pos

    distinct_positions, visited = walk(area, pos, direction)
    print(f'Visited {distinct_positions} distinct positions.')

    obstructions = 0
    for y, line in enumerate(area):
        print(f'Processing line {y}')
        for x, char in enumerate(line):
            if char == '#' or (x, y) == pos:
                continue
            if (x, y) not in visited:
                continue
            area_copy = area.copy()
            line_copy = area_copy[y]
            line_copy = line_copy[:x] + '#' + line_copy[x + 1:]
            area_copy[y] = line_copy
            if walk(area_copy, pos, direction)[0] == -1:
                obstructions += 1

    print(f'{obstructions} possible obstructions')

if __name__ == '__main__':
    main()

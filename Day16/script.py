from dataclasses import dataclass
import os
from astar import find_path
os.chdir(os.path.dirname(__file__))

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    direction: str # h or v

    def up(self):
        return Point(self.x, self.y - 1, 'v')

    def down(self):
        return Point(self.x, self.y + 1, 'v')

    def left(self):
        return Point(self.x - 1, self.y, 'h')

    def right(self):
        return Point(self.x + 1, self.y, 'h')

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        tiles = [line.strip() for line in f.readlines()]

    start_x, start_y = find(tiles, 'S')
    end_x, end_y = find(tiles, 'E')
    start = Point(start_x, start_y, 'h')
    end1 = Point(end_x, end_y, 'h')
    end2 = Point(end_x, end_y, 'v')
    print_score(tiles, start, end1)
    print_score(tiles, start, end2)

def print_score(tiles, start, end):
    result = find_path(
        start,
        end,
        neighbors_fnct=lambda p: get_neighbors(p, tiles),
        distance_between_fnct=lambda p1, p2: get_distance(p1, p2),
        heuristic_cost_estimate_fnct=lambda _, __: 0.0
    )
    result_list = list(result)
    score = 0
    for p1, p2 in zip(result_list, result_list[1::]):
        score += get_distance(p1, p2)
    print(score)

def get_neighbors(p: Point, tiles):
    yield Point(p.x, p.y, 'h' if p.direction == 'v' else 'v')
    if p.direction == 'h':
        left = p.left()
        if tiles[left.y][left.x] != '#':
            yield left
        right = p.right()
        if tiles[right.y][right.x] != '#':
            yield right
    elif p.direction == 'v':
        up = p.up()
        if tiles[up.y][up.x] != '#':
            yield up
        down = p.down()
        if tiles[down.y][down.x] != '#':
            yield down
    else:
        assert False

def get_distance(p1: Point, p2: Point):
    if p1.direction == p2.direction:
        return 1
    return 1000

def find(tiles: list[str], char: str) -> tuple[int, int]:
    for y, line in enumerate(tiles):
        for x, current in enumerate(line):
            if current == char:
                return (x, y)
    assert False

if __name__ == '__main__':
    main()

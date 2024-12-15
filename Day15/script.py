from dataclasses import dataclass
import os
os.chdir(os.path.dirname(__file__))

@dataclass
class Point:
    x: int
    y: int

    def add(self, v: 'Vector') -> 'Point':
        return Point(self.x + v.x, self.y + v.y)

@dataclass
class Vector:
    x: int
    y: int

def main():
    area_map: list[list[str]] = []
    instructions: str = ''
    with open('input.txt', 'r', encoding='utf-8') as f:
        read_map = True
        for line in f.readlines():
            line = line.strip()
            if not line:
                read_map = False
            if read_map:
                area_map.append(list(line))
            else:
                instructions += line

    bot = None
    for y, line in enumerate(area_map):
        for x, char in enumerate(line):
            if char == '@':
                bot = Point(x, y)
                break
        if bot is not None:
            break
    assert bot

    for instruction in instructions:
        vector = get_vector(instruction)
        new_pos = try_move(bot, vector, area_map)
        if new_pos is not None:
            bot = new_pos

    gps_sum = 0
    for y, line in enumerate(area_map):
        for x, char in enumerate(line):
            if char == 'O':
                gps_sum += 100 * y + x

    print(f'Sum of GPS coordinates: {gps_sum}')

def try_move(pos: Point, v: Vector, area_map: list[list[str]]) -> Point | None:
    to_pos = pos.add(v)
    to_char = area_map[to_pos.y][to_pos.x]
    if to_char == '.':
        swap(pos, to_pos, area_map)
        return to_pos
    elif to_char == 'O':
        if try_move(to_pos, v, area_map) is not None:
            swap(pos, to_pos, area_map)
            return to_pos
        return None
    elif to_char == '#':
        return None
    else:
        raise ValueError(f'Unknown char {to_char}')

def swap(p_from: Point, p_to: Point, area_map: list[list[str]]):
    area_map[p_to.y][p_to.x], area_map[p_from.y][p_from.x] = area_map[p_from.y][p_from.x], area_map[p_to.y][p_to.x]

def get_vector(instruction) -> Vector:
    match instruction:
        case '^':
            return Vector(0, -1)
        case 'v':
            return Vector(0, 1)
        case '>':
            return Vector(1, 0)
        case '<':
            return Vector(-1, 0)

if __name__ == '__main__':
    main()

from dataclasses import dataclass
import os
os.chdir(os.path.dirname(__file__))

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def add(self, v: 'Vector') -> 'Point':
        return Point(self.x + v.x, self.y + v.y)

@dataclass
class Vector:
    x: int
    y: int

    def invert(self) -> 'Vector':
        return Vector(self.x * -1, self.y * -1)

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
    original_area_map = [line.copy() for line in area_map]

    bot = find_bot(area_map)
    for instruction in instructions:
        vector = get_vector(instruction)
        new_pos = try_move(bot, vector, area_map)
        if new_pos is not None:
            bot = new_pos

    gps_sum = calculate_gps_sum(area_map, 'O')
    print(f'Sum of GPS coordinates (part 1): {gps_sum}')

    area_map = []
    for original_line in original_area_map:
        line = []
        area_map.append(line)
        for original_char in original_line:
            match original_char:
                case '#':
                    line.extend(('#', '#'))
                case 'O':
                    line.extend(('[', ']'))
                case '.':
                    line.extend(('.', '.'))
                case '@':
                    line.extend(('@', '.'))

    bot = find_bot(area_map)
    for i, instruction in enumerate(instructions):
        vector = get_vector(instruction)
        if can_move(bot, vector, area_map):
            new_pos = move(bot, vector, area_map)
            assert new_pos
            bot = new_pos
            check_map_valid(area_map)

    gps_sum = calculate_gps_sum(area_map, '[')
    print(f'Sum of GPS coordinates (part 2): {gps_sum}')

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

def can_move(pos: Point, v: Vector, area_map: list[list[str]], partner_approved=False) -> bool:
    to_pos = pos.add(v)
    to_char = area_map[to_pos.y][to_pos.x]
    if to_char == '.':
        return True
    elif to_char == 'O':
        return can_move(to_pos, v, area_map)
    elif to_char == '[':
        return can_move(to_pos, v, area_map) and (partner_approved or can_move(to_pos.add(Vector(1, 0)), v, area_map, partner_approved=True))
    elif to_char == ']':
        return can_move(to_pos, v, area_map) and (partner_approved or can_move(to_pos.add(Vector(-1, 0)), v, area_map, partner_approved=True))
    elif to_char == '#':
        return False
    else:
        raise ValueError(f'Unknown char {to_char}')

def move(from_pos: Point, v: Vector, area_map: list[list[str]]) -> Point:
    to_pos = from_pos.add(v)
    to_char = area_map[to_pos.y][to_pos.x]

    if v.y == 0:
        # Horizontal movement:
        # Go over all boxes to find first free position,
        # then drag all the boxes to there.
        free_pos = from_pos
        while area_map[free_pos.y][free_pos.x] != '.':
            free_pos = free_pos.add(v)
        while free_pos != from_pos:
            next_pos = free_pos.add(v.invert())
            swap(free_pos, next_pos, area_map)
            free_pos = next_pos
        return from_pos.add(v)

    if to_char == '.':
        # Nothing's in the way, just swap.
        swap(from_pos, to_pos, area_map)
        return to_pos

    assert to_char in '[]'

    # Vertical movement:
    # Collect all boxes that will be pushed by our movement,
    # then move them in the target direction, starting from the end.
    push_points: dict[Point, None] = {}
    try:
        add_push_points(to_pos, v, push_points, area_map)
    except LookupError:
        return from_pos
    for push_point in sorted(push_points.keys(), key=lambda p: p.y, reverse=v.y == 1):
        swap(push_point, push_point.add(v), area_map)
    swap(from_pos, to_pos, area_map)

    return to_pos

def add_push_points(pos: Point, v: Vector, push_points: dict[Point, None], area_map: list[list[str]]):
    pos_char = area_map[pos.y][pos.x]
    if pos_char == '[':
        other_pos = pos.add(Vector(1, 0))
        push_points[pos] = None
        push_points[other_pos] = None
        add_push_points(pos.add(v), v, push_points, area_map)
        add_push_points(other_pos.add(v), v, push_points, area_map)
    elif pos_char == ']':
        other_pos = pos.add(Vector(-1, 0))
        push_points[pos] = None
        push_points[other_pos] = None
        add_push_points(pos.add(v), v, push_points, area_map)
        add_push_points(other_pos.add(v), v, push_points, area_map)
    else:
        if pos_char != '.':
            # This should have been caught by can_move, but it wasn't...
            raise LookupError()

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

def find_bot(area_map):
    for y, line in enumerate(area_map):
        for x, char in enumerate(line):
            if char == '@':
                return Point(x, y)
    assert False

def calculate_gps_sum(area_map, box_char):
    gps_sum = 0
    for y, original_line in enumerate(area_map):
        for x, char in enumerate(original_line):
            if char == box_char:
                gps_sum += 100 * y + x
    return gps_sum

def print_map(area_map: list[list[str]]):
    for line in area_map:
        print(''.join(line))
    print()

def check_map_valid(area_map: list[list[str]]):
    for y, line in enumerate(area_map):
        for x, char in enumerate(line):
            if char == '[':
                assert area_map[y][x + 1] == ']'

if __name__ == '__main__':
    main()

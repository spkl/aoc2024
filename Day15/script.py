import os
os.chdir(os.path.dirname(__file__))

def main():
    map: list[list[str]] = []
    instructions: str = ''
    with open('input.txt', 'r', encoding='utf-8') as f:
        read_map = True
        for line in f.readlines():
            line = line.strip()
            if not line:
                read_map = False
            if read_map:
                map.append(list(line))
            else:
                instructions += line

    bot = None
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == '@':
                bot = (x, y)
                break
        if bot is not None:
            break
    assert bot

    for instruction in instructions:
        vector = get_vector(instruction)
        char, pos = find_space_or_wall(bot, vector, map)
        if char == '#':
            continue
        assert char == '.'
        from_x, from_y = pos
        while True:
            to_x, to_y = (from_x + vector[0] * -1, from_y + vector[1] * -1)
            map[to_y][to_x], map[from_y][from_x] = map[from_y][from_x], map[to_y][to_x]
            if (to_x, to_y) == bot:
                bot = (from_x, from_y)
                break
            from_x, from_y = to_x, to_y

    gps_sum = 0
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == 'O':
                gps_sum += 100 * y + x

    print(f'Sum of GPS coordinates: {gps_sum}')

def find_space_or_wall(pos: tuple[int, int], vector: tuple[int, int], map: list[list[str]]):
    x, y = pos
    while True:
        x, y = (x + vector[0], y + vector[1])
        char = map[y][x]
        if char in ('.', '#'):
            return char, (x, y)

def get_vector(instruction):
    match instruction:
        case '^':
            return (0, -1)
        case 'v':
            return (0, 1)
        case '>':
            return (1, 0)
        case '<':
            return (-1, 0)

if __name__ == '__main__':
    main()

import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        racetrack = [line.strip() for line in f.readlines()]

    start = find_char(racetrack, 'S')
    tile_positions = follow_track(racetrack, start)
    print(f'Track length without cheating is {max(tile_positions.values())}.')

    max_y = len(racetrack) - 1
    max_x = len(racetrack[0]) - 1
    cheats: dict[int, list[tuple[int, int]]] = {}
    for y, line in enumerate(racetrack):
        for x, char in enumerate(line):
            if char != '#':
                continue
            a, b = None, None
            if 0 < y < max_y and racetrack[y - 1][x] != '#' and racetrack[y + 1][x] != '#':
                a, b = (x, y - 1), (x, y + 1)
            elif 0 < x < max_x and racetrack[y][x - 1] != '#' and racetrack[y][x + 1] != '#':
                a, b = (x - 1, y), (x + 1, y)
            if a is not None and b is not None:
                pos_a = tile_positions[a]
                pos_b = tile_positions[b]
                before = min(pos_a, pos_b)
                after = max(pos_a, pos_b)
                picoseconds_saved = after - before - 2
                cheats.setdefault(picoseconds_saved, [])
                cheats[picoseconds_saved].append((x, y))

    print('Possible cheats (picoseconds saved, positions):')
    print(sorted(((item[0], len(item[1])) for item in cheats.items()), key=lambda item: item[0]))

    n_best_cheats = 0
    for picoseconds_saved, positions in cheats.items():
        if picoseconds_saved >= 100:
            n_best_cheats += len(positions)
    print(f'Number of best cheats: {n_best_cheats}')

def find_char(lines: list[str], char: str) -> tuple[int, int]:
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == char:
                return (x, y)
    assert False

def follow_track(racetrack: list[str], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    tile_positions: dict[tuple[int, int], int] = {}
    current = start
    i = 0
    while True:
        tile_positions[current] = i
        i += 1
        x, y = current
        if racetrack[y][x] == 'E':
            break
        if (x - 1, y) not in tile_positions and racetrack[y][x - 1] != '#':
            current = (x - 1, y)
        elif (x + 1, y) not in tile_positions and racetrack[y][x + 1] != '#':
            current = (x + 1, y)
        elif (x, y - 1) not in tile_positions and racetrack[y - 1][x] != '#':
            current = (x, y - 1)
        elif (x, y + 1) not in tile_positions and racetrack[y + 1][x] != '#':
            current = (x, y + 1)
        else:
            assert False
    return tile_positions

if __name__ == '__main__':
    main()

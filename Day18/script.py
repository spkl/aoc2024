from astar import find_path
import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        max_x, max_y = map(int, f.readline().strip().split('x'))
        incoming = [tuple(map(int, pos.strip().split(','))) for pos in f.readlines()]

    fallen_bytes = 1024
    corrupted = set(incoming[:fallen_bytes])
    start = (0, 0)
    end = (max_x, max_y)

    path = get_path(corrupted, start, end)
    print(f'Minimum number of steps after {fallen_bytes} fallen bytes: {len(path) - 1}')

    for fallen_byte in incoming[fallen_bytes:]:
        corrupted.add(fallen_byte)
        if fallen_byte not in path:
            continue
        path = get_path(corrupted, start, end)
        if path is None:
            print(f'The byte at {fallen_byte} cuts off the path.')
            break

def get_path(corrupted, start, end):
    path = find_path(
        start,
        end,
        neighbors_fnct=lambda pos: get_neighbors(pos, start, end, corrupted),
        heuristic_cost_estimate_fnct=lambda _, __: 0.0,
        distance_between_fnct=lambda _, __: 0.0
    )

    return list(path) if path is not None else None

def get_neighbors(pos, min_pos, max_pos, corrupted):
    x, y = pos
    min_x, min_y = min_pos
    max_x, max_y = max_pos
    if x > min_x and (x - 1, y) not in corrupted:
        yield (x - 1, y)
    if x < max_x and (x + 1, y) not in corrupted:
        yield (x + 1, y)
    if y > min_y and (x, y - 1) not in corrupted:
        yield (x, y - 1)
    if y < max_y and (x, y + 1) not in corrupted:
        yield (x, y + 1)

if __name__ == '__main__':
    main()

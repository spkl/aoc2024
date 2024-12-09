import os
from itertools import repeat, takewhile
os.chdir(os.path.dirname(__file__))

def remove_last_nonempty_value(blocks: list[int]) -> int|None:
    while blocks[-1] == -1:
        del blocks[-1]
    value = blocks[-1]
    del blocks[-1]
    return value

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        disk_map = f.read().strip()

    blocks: list[int] = []
    empty = False
    file_id = 0
    for v in disk_map:
        v = int(v)
        if empty:
            blocks.extend(repeat(-1, v))
        else:
            blocks.extend(repeat(file_id, v))
            file_id += 1
        empty = not empty

    blocks1 = blocks.copy()
    empty_index = 0
    while True:
        try:
            empty_index = blocks1.index(-1, empty_index)
            value = remove_last_nonempty_value(blocks1)
            blocks1[empty_index] = value
        except ValueError:
            break

    print(f'Checksum 1: {sum(i * v for i, v in enumerate(blocks1))}')

    blocks2 = blocks.copy()
    file_id = next(x for x in reversed(blocks2) if x != -1)
    while file_id > 0:
        file_index = blocks2.index(file_id)
        file_length = sum(1 for _ in takewhile(lambda x: x == file_id, blocks2[file_index:]))
        candidate_blocks = blocks2[:file_index]
        consecutive_empty = 0
        to_index = None
        for i, value in enumerate(candidate_blocks):
            if value == -1:
                consecutive_empty += 1
                if consecutive_empty == file_length:
                    to_index = i - (consecutive_empty - 1)
                    break
            else:
                consecutive_empty = 0
        if to_index is not None:
            blocks2[file_index:file_index + file_length] = list(repeat(-1, file_length))
            blocks2[to_index:to_index + file_length] = list(repeat(file_id, file_length))
        file_id -= 1

    print(f'Checksum 2: {sum(i * v for i, v in enumerate(blocks2) if v != -1)}')

if __name__ == '__main__':
    main()

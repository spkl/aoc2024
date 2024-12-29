import os
import itertools
os.chdir(os.path.dirname(__file__))

ITEM_HEIGHT = 7

def main():
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = iter(line.strip() for line in f.readlines())

        while True:
            item = list(itertools.islice(lines, ITEM_HEIGHT))
            heights: list[int] = []
            if item[0][0] == '#':
                # lock
                for x in range(len(item[0])):
                    for y in range(ITEM_HEIGHT):
                        if item[y][x] == '.':
                            heights.append(y - 1)
                            break
                locks.append(heights)
            else:
                # key
                for x in range(len(item[0])):
                    for y in range(ITEM_HEIGHT):
                        if item[y][x] == '#':
                            heights.append(ITEM_HEIGHT - y - 1)
                            break
                keys.append(heights)
            if next(lines, None) is None:
                break

    fitting_combinations = 0
    for key, lock in itertools.product(keys, locks):
        fits = True
        for key_height, lock_height in zip(key, lock):
            if (key_height + lock_height) >= ITEM_HEIGHT - 1:
                fits = False
                break
        if fits:
            fitting_combinations += 1
    print(f'There are {fitting_combinations} key/lock combinations that fit.')

if __name__ == '__main__':
    main()

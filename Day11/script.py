import os
os.chdir(os.path.dirname(__file__))

TOTAL_BLINKS = 75
solutions: dict[str, dict[int, int]] = {} # stone: blinks: resulting number of stones

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        original_stones = f.read().strip().split()

    n_stones = 0
    for stone in original_stones:
        n_stones += solve(stone, TOTAL_BLINKS)
    print(n_stones)

def solve(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone in solutions and blinks in solutions[stone]:
        return solutions[stone][blinks]

    if stone == '0':
        solution = solve('1', blinks - 1)
    elif len(stone) % 2 == 0:
        left_stone = stone[:len(stone)//2]
        right_stone = stone[len(stone)//2:]
        while len(right_stone) > 1 and right_stone[0] == '0':
            right_stone = right_stone[1:]
        solution = solve(left_stone, blinks - 1) + solve(right_stone, blinks - 1)
    else:
        solution = solve(str(int(stone) * 2024), blinks - 1)

    if stone not in solutions:
        solutions[stone] = {}
    solutions[stone][blinks] = solution
    return solution

if __name__ == '__main__':
    main()

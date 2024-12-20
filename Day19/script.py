import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        towels = list(f.readline().strip().split(', '))
        _ = f.readline()
        designs = [design.strip() for design in f.readlines()]

    possible_designs = [d for d in designs if is_possible(d, towels)]
    print(f'Number of possible designs: {len(possible_designs)}')

def is_possible(design: str, towels: list[str]) -> bool:
    if len(design) == 0:
        return True

    for towel in towels:
        if design.startswith(towel):
            if is_possible(design[len(towel):], towels):
                return True

    return False

if __name__ == '__main__':
    main()

import os
import itertools
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        connections = [line.strip() for line in f.readlines()]

    connected_computers: dict[str, set[str]] = {}
    for connection in connections:
        c1, c2 = connection.split('-')
        connected_computers.setdefault(c1, set())
        connected_computers[c1].add(c2)
        connected_computers.setdefault(c2, set())
        connected_computers[c2].add(c1)

    n_computer_sets_with_t = 0
    for c1, c2, c3 in itertools.combinations(connected_computers.keys(), 3):
        if c2 in connected_computers[c1] and c3 in connected_computers[c1] \
            and c1 in connected_computers[c2] and c3 in connected_computers[c2] \
            and c1 in connected_computers[c3] and c2 in connected_computers[c3]:
            if c1.startswith('t') or c2.startswith('t') or c3.startswith('t'):
                n_computer_sets_with_t += 1

    print(f'There are {n_computer_sets_with_t} sets of three connected computers where at least one has a t in it')

if __name__ == '__main__':
    main()

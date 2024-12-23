import os
from networkx.algorithms.clique import enumerate_all_cliques, max_weight_clique
from networkx import to_networkx_graph
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

    graph = to_networkx_graph(connected_computers)

    n_computer_sets_with_t = 0
    for network in enumerate_all_cliques(graph):
        if len(network) > 3:
            break
        if len(network) == 3:
            if any(computer for computer in network if computer.startswith('t')):
                n_computer_sets_with_t += 1

    print(f'There are {n_computer_sets_with_t} sets of three connected computers where at least one has a t in it')

    largest_network, _ = max_weight_clique(graph, weight=None)
    print(','.join(sorted(largest_network)))

if __name__ == '__main__':
    main()

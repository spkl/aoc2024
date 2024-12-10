import os
os.chdir(os.path.dirname(__file__))

def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        topo_map = [line.strip() for line in f.readlines()]

    score_sum = 0
    rating_sum = 0
    for y, line in enumerate(topo_map):
        for x, char in enumerate(line):
            if char == '0':
                score, rating = search_peaks(topo_map, (x, y))
                score_sum += score
                rating_sum += rating

    print(f'Sum of trailhead scores (part 1) = {score_sum}')
    print(f'Sum of trailhead ratings (part 2) = {rating_sum}')

def search_peaks(topo_map: list[str], trailhead: tuple[int, int]) -> tuple[int, int]:
    t = trails(topo_map)
    t.hike(trailhead)
    return len(set(t.peaks)), len(t.peaks)

class trails:
    def __init__(self, topo_map: list[str]):
        self.topo_map = topo_map
        self.peaks: list[tuple[int, int]] = []
        self.path: list[tuple[int, int]] = []
        self.min_x = 0
        self.max_x = len(self.topo_map[0]) - 1
        self.min_y = 0
        self.max_y = len(self.topo_map) - 1

    def hike(self, trailhead: tuple[int, int]):
        self.path.append(trailhead)
        self.walk()

    def walk(self):
        x, y = self.path[-1]
        if self.topo_map[y][x] == '9':
            self.peaks.append((x, y))
        else:
            self.try_walk(x - 1, y)
            self.try_walk(x + 1, y)
            self.try_walk(x, y - 1)
            self.try_walk(x, y + 1)

    def try_walk(self, nx, ny):
        x, y = self.path[-1]
        if nx >= self.min_x and nx <= self.max_x and ny >= self.min_y and ny <= self.max_y:
            if int(self.topo_map[ny][nx]) == int(self.topo_map[y][x]) + 1:
                if (nx, ny) not in self.path:
                    self.path.append((nx, ny))
                    self.walk()
                    self.path.pop()

if __name__ == '__main__':
    main()

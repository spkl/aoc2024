from dataclasses import dataclass, field
import os
os.chdir(os.path.dirname(__file__))

@dataclass
class Plot:
    plant: str
    coord: tuple[int, int]
    region: 'Region' = None

@dataclass
class Region:
    plant: str
    garden: 'Garden'
    plots: list[Plot] = field(default_factory=lambda: [])

    def add_plot(self, plot: Plot) -> None:
        self.plots.append(plot)
        plot.region = self

        x, y = plot.coord
        self.try_add_plot(x + 1, y)
        self.try_add_plot(x - 1, y)
        self.try_add_plot(x, y + 1)
        self.try_add_plot(x, y - 1)

    def try_add_plot(self, x, y) -> None:
        plot = self.garden.plots.get((x, y))
        if plot is None:
            return
        if plot.region is not None:
            return
        if plot.plant != self.plant:
            return
        self.add_plot(plot)

    def area(self) -> int:
        return len(self.plots)

    def perimeter(self) -> int:
        sum = 0
        for plot in self.plots:
            x, y = plot.coord
            if not self.in_region((x + 1, y)):
                sum += 1
            if not self.in_region((x - 1, y)):
                sum += 1
            if not self.in_region((x, y + 1)):
                sum += 1
            if not self.in_region((x, y - 1)):
                sum += 1
        return sum

    def in_region(self, coord: tuple[int, int]) -> bool:
        plot = self.garden.plots.get(coord)
        if plot is None:
            return False
        return plot.region == self

@dataclass
class Garden:
    regions: list[Region] = field(default_factory=lambda: [])
    plots: dict[tuple[int, int], Plot] = field(default_factory=lambda: {})

    def new_region(self, plant: str) -> Region:
        region = Region(plant, self)
        self.regions.append(region)
        return region

def main():
    garden = Garden()
    with open('input.txt', 'r', encoding='utf-8') as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, plant in enumerate(line):
                plot = Plot(plant, (x, y))
                garden.plots[plot.coord] = plot

    for plot in garden.plots.values():
        if plot.region is not None:
            continue
        region = garden.new_region(plot.plant)
        region.add_plot(plot)

    price = sum(r.area() * r.perimeter() for r in garden.regions)
    print(f'Price: {price}')

if __name__ == '__main__':
    main()

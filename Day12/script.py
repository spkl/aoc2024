from dataclasses import dataclass, field
from typing import Callable
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

    def sides(self) -> int:
        top = ((0, -1), (1, 0), (-1, 0), lambda plot: plot.coord[0])
        bottom = ((0, 1), (1, 0), (-1, 0), lambda plot: plot.coord[0])
        left = ((-1, 0), (0, 1), (0, -1), lambda plot: plot.coord[1])
        right = ((1, 0), (0, 1), (0, -1), lambda plot: plot.coord[1])
        all_sides = [top, bottom, left, right]
        return sum(len(self.group_by_side(*side)) for side in all_sides)

    def group_by_side(self,
            check: tuple[int, int],
            neighbor1: tuple[int, int],
            neighbor2: tuple[int, int],
            sort_key: Callable[[Plot], int]) -> list[set[tuple[int, int]]]:
        # Approach:
        # Get all plots that have a fence on the 'check' side.
        # Build groups of plots are neighbors on either side (neighbor1, neighbor2).
        # For the loop to work, the plots have to be sorted by X or Y coordinate, depending on what the 'check' side is.
        # For example, if we check the top side, plots are ordered by X coordinate, so that the groups can be built up from left to right.
        # Otherwise we might build more groups than we want, because the direct neighbor was not part of the correct group (yet).
        plots = [plot for plot in self.plots if not self.in_region((plot.coord[0] + check[0], plot.coord[1] + check[1]))]
        groups: list[set[tuple[int, int]]] = []
        for plot in sorted(plots, key=sort_key):
            x, y = plot.coord
            group = next((group for group in groups
                          if (x + neighbor1[0], y + neighbor1[1]) in group
                          or (x + neighbor2[0], y + neighbor2[1]) in group), None)
            if group is None:
                group = set()
                groups.append(group)
            group.add((x, y))
        return groups

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
    discounted_price = sum(r.area() * r.sides() for r in garden.regions)
    print(f'Price: {price}')
    print(f'Discounted price: {discounted_price}')

if __name__ == '__main__':
    main()

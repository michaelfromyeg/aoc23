"""
https://adventofcode.com/2023/day/14
"""
from enum import Enum

from tqdm import tqdm

from utils.read import read

DEBUG = True
DAY = 14

Grid = list[list[str]]

CYCLES = 1000000000


def print_grid(grid: Grid) -> None:
    """
    Print a grid, nicely.
    """
    for row in grid:
        print("".join(row))
    print()


class Direction(Enum):
    """
    Which direction to rotate in.
    """

    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


def slide(grid: Grid, i: int, j: int, direction: Direction) -> None:
    """
    Slide a round rock north.
    """
    match direction:
        case Direction.NORTH:
            curr = i

            while curr > 0 and grid[curr][j] == "O" and grid[curr - 1][j] == ".":
                grid[curr][j], grid[curr - 1][j] = ".", "O"

                curr -= 1

            return None
        case _:
            return None


def slide_all(grid: Grid, direction: Direction) -> None:
    """
    Rotate the grid in every direction.
    """
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "O":
                slide(grid, i, j, direction)


def get_grid() -> Grid:
    """
    Parse the grid.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    grid: Grid = []
    for line in lines:
        line = line.strip()

        row = []
        for c in line:
            row.append(c)
        grid.append(row)

    if DEBUG:
        print_grid(grid)

    return grid


def solve1() -> int:
    """
    Slide the rocks up.
    """
    grid = get_grid()

    slide_all(grid, Direction.NORTH)

    if DEBUG:
        print_grid(grid)

    total = 0
    n = len(grid)
    for i, row in enumerate(grid):
        n_rocks = sum([1 for c in row if c == "O"])
        total += n_rocks * (n - i)

    return total


def cycle(grid: Grid) -> None:
    """
    Slide in every dierction.
    """
    slide_all(grid, Direction.NORTH)
    # slide_all(grid, Direction.WEST)
    # slide_all(grid, Direction.SOUTH)
    # slide_all(grid, Direction.EAST)


def solve2() -> int:
    """
    Cycle the grid, a lot.
    """
    grid = get_grid()

    for _ in tqdm(range(CYCLES)):
        cycle(grid)

    return 0


if __name__ == "__main__":
    print(solve1())
    print(solve2())

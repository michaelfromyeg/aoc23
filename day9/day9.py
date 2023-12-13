"""
https://adventofcode.com/2023/day/9
"""
import pprint

from utils.read import read

DEBUG = True
DAY = 9


def roll(arr: list[int], k: int) -> list[int]:
    """
    Shift an array k-elements forward.
    """
    n = len(arr)
    k = k % n
    return arr[-k:] + arr[:-k]


def get_value(values: list[int], forward: bool = True) -> int:
    """
    Determine the next value in sequence.
    """
    # I'll start with the naive approach

    n = len(values)

    grid = []
    for _ in range(n + 1):
        rows = []
        for _ in range(n + 1):
            rows.append(0)
        grid.append(rows)

    for i, value in enumerate(values):
        grid[0][i] = value

    for row in range(1, n + 1):
        for col in range(n - row):
            grid[row][col] = grid[row - 1][col + 1] - grid[row - 1][col]

    if forward:
        for row in range(n - 1, -1, -1):
            last_col = n - row
            grid[row][last_col] = grid[row][last_col - 1] + grid[row + 1][last_col - 1]
    else:
        # TODO(michaelfromyeg): figure out indexing for this one
        for i, row in enumerate(grid):
            grid[i] = [row[-1]] + row[:-1]

    if DEBUG:
        pprint.pprint(grid)

    return grid[0][-1]


def solve1() -> int:
    """ """
    lines = read(DAY, 1 if DEBUG else 0)

    total = 0
    for line in lines:
        values = [int(v) for v in line.strip().split(" ")]
        next_value = get_value(values)

        total += next_value

    return total


def solve2() -> int:
    """ """
    lines = read(DAY, 1 if DEBUG else 0)

    total = 0
    for line in lines:
        values = [int(v) for v in line.strip().split(" ")]
        next_value = get_value(values, forward=False)

        total += next_value

    return total


if __name__ == "__main__":
    # print(solve1())
    print(solve2())

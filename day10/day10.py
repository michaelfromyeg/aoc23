"""
https://adventofcode.com/2023/day/10
"""
from __future__ import annotations

import pprint
from collections import deque
from enum import Enum

from utils.read import read

DAY = 10

DEBUG = False
TEST = 1

Point = tuple[int, int]


class Direction(Enum):
    """
    The cardinal directions.
    """

    N = 0
    E = 1
    S = 2
    W = 3


class Pipe(Enum):
    """
    The kinds of pipes in the map.
    """

    NS = "|"
    EW = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"

    START = "S"
    GROUND = "."

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


def str2pipe(c: str) -> Pipe:
    """
    Convert a string to a Pipe.
    """
    match c:
        case "|":
            return Pipe.NS
        case "-":
            return Pipe.EW
        case "L":
            return Pipe.NE
        case "J":
            return Pipe.NW
        case "7":
            return Pipe.SW
        case "F":
            return Pipe.SE
        case "S":
            return Pipe.START
        case ".":
            return Pipe.GROUND
        case _:
            raise ValueError(f"{c} is not a pipe")


SOUTHS = [Pipe.NS, Pipe.SW, Pipe.SE]
NORTHS = [Pipe.NS, Pipe.NW, Pipe.NE]
EASTS = [Pipe.EW, Pipe.NE, Pipe.SE]
WESTS = [Pipe.EW, Pipe.NW, Pipe.SW]


def connectors(direction: Direction) -> tuple[list[Pipe], list[Pipe]]:
    """
    Get the pipes connecting in the other direction.
    """
    match direction:
        case Direction.N:
            return (NORTHS, SOUTHS)
        case Direction.S:
            return (SOUTHS, NORTHS)
        case Direction.E:
            return (EASTS, WESTS)
        case Direction.W:
            return (WESTS, EASTS)
        case _:
            raise ValueError(f"{direction} is not a direction")


def connects(self: Pipe, other: Pipe, direction: Direction) -> bool:
    """
    Check if two pipes connect in a direction.
    """
    # if self == Pipe.START and other != Pipe.GROUND:
    #     return True
    # if other == Pipe.START:
    #     return True

    self_ways, other_ways = connectors(direction)
    return self in self_ways and other in other_ways


def neighbors(grid: list[list[Pipe]], point: Point) -> list[Point]:
    """
    Get the neighbors for a point in the grid.
    """
    ns: list[Point] = []

    x, y = point
    self = grid[x][y]

    min_x, max_x, min_y, max_y = -1, len(grid), -1, len(grid[0])

    if x - 1 > min_x and connects(self, grid[x - 1][y], Direction.N):
        ns.append((x - 1, y))
    if x + 1 < max_x and connects(self, grid[x + 1][y], Direction.S):
        ns.append((x + 1, y))

    if y - 1 > min_y and connects(self, grid[x][y - 1], Direction.W):
        ns.append((x, y - 1))
    if y + 1 < max_y and connects(self, grid[x][y + 1], Direction.E):
        ns.append((x, y + 1))

    return ns


def find_max_depth_along_ring(
    parent: dict[Point, Point], depth: dict[Point, int]
) -> int:
    """
    As title.
    """
    return 0


def bfs(grid: list[list[Pipe]], s: Point) -> int:
    """
    Perform BFS on the grid, from the starting point.
    """
    visited: set[Point] = set()

    parent: dict[Point, Point] = {}
    depth: dict[Point, int] = {}

    queue = deque([(s, 0)])

    while queue:
        curr_point, curr_depth = queue.pop()

        if curr_point not in visited:
            visited.add(curr_point)

            depth[curr_point] = curr_depth

            for neighbor in neighbors(grid, curr_point):
                if neighbor not in visited:
                    queue.append((neighbor, curr_depth + 1))
                    parent[neighbor] = curr_point

    if DEBUG:
        pprint.pprint(parent)
        pprint.pprint(depth)

    return find_max_depth_along_ring(parent, depth)


def dfs(grid: list[list[Pipe]], s: Point) -> int | None:
    """
    Perform iterative DFS. Try to find the start again.
    s is the start point.
    """

    stack: list[tuple[Point, list[Point]]] = [
        (s, [s])
    ]  # Stack to store the current node and the path to reach it
    visited = set()  # Set to keep track of visited nodes

    while stack:
        current_point, path = stack.pop()

        if DEBUG:
            print(f"Trying {current_point} from {path}")

        # the >3 is a complete hack...
        if current_point == s and len(path) > 3 and path[-1] == s:
            if DEBUG:
                print("".join([str(grid[i][j]) for i, j in path]))

            return len(path) // 2

        if current_point in visited:
            continue

        visited.add(current_point)

        for neighbor in neighbors(grid, current_point):
            stack.append((neighbor, path + [neighbor]))

    return None


def solve1() -> int:
    """
    Do a kind of DFS, I think.
    """
    lines = read(DAY, TEST if DEBUG else 0)

    s: Point | None = None
    grid: list[list[Pipe]] = []
    for row_idx, line in enumerate(lines):
        row: list[Pipe] = []
        for col_idx, c in enumerate(line.strip()):
            p = str2pipe(c)
            if p == Pipe.START:
                s = (row_idx, col_idx)
            row.append(p)
        grid.append(row)

    if DEBUG:
        pprint.pprint(grid)

    if s is None:
        raise ValueError("No S in grid")

    # This is so dumb but it works...
    cmax = 0
    for pipe in ["|", "-", "L", "J", "7", "F"]:
        grid[s[0]][s[1]] = str2pipe(pipe)
        cmax = max(dfs(grid, s) or 0, cmax)

    return cmax


def solve2() -> int:
    """ """
    lines = read(DAY, TEST if DEBUG else 0)

    return 0


if __name__ == "__main__":
    print(solve1())
    print(solve2())

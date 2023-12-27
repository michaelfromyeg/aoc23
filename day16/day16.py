"""
https://adventofcode.com/2023/day/16
"""
from collections import deque
from enum import IntEnum, StrEnum
from typing import Any

from utils.read import read

DEBUG = False
TEST = 1

DAY = 16


class Direction(IntEnum):
    """
    A cardinal direction.

        N
    W       E
        S
    """

    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    def delta(self) -> tuple[int, int]:
        """
        Return a two-int tuples representing (dx, dy).
        """
        match self:
            case Direction.NORTH:
                return (-1, 0)
            case Direction.EAST:
                return (0, 1)
            case Direction.SOUTH:
                return (1, 0)
            case Direction.WEST:
                return (0, -1)
            case _:
                raise ValueError("Built impossible direction")


HORIZONTAL = [Direction.EAST, Direction.WEST]
VERTICAL = [Direction.NORTH, Direction.SOUTH]


class Object(StrEnum):
    """
    Something that exists on our grid.
    """

    E = "."  # empty

    VSPLITTER = "|"
    HSPLITTER = "-"

    FMIRROR = "/"
    BMIRROR = "\\"


def str2object(c: str) -> Object:
    """
    Convert an object to a string.
    """
    match c:
        case ".":
            return Object.E
        case "|":
            return Object.VSPLITTER
        case "-":
            return Object.HSPLITTER
        case "/":
            return Object.FMIRROR
        case "\\":
            return Object.BMIRROR
        case _:
            raise ValueError(f"Invalid object {c} in map")


Grid = list[list[Any]]
ObjectGrid = list[list[Object]]

Beam = tuple[int, int, Direction]


def print_grid(grid: Grid) -> None:
    """
    Display the grid, for debugging.
    """
    for row in grid:
        print("".join(str(c) for c in row))
    print()


def get_grid() -> ObjectGrid:
    """
    Build the grid.
    """
    lines = read(DAY, TEST if DEBUG else 0)

    grid: Grid = []

    for line in lines:
        line = line.strip()

        row: list[Object] = []
        for c in line:
            row.append(str2object(c))

        grid.append(row)

    return grid


def neighbors(grid: ObjectGrid, beam: Beam) -> list[Beam]:
    """
    Get the neighbors from this beam.

    Note we have to respect the beam's direction and check for splitters.

    The logic here needs to check the existing grid value to deal with the beams direction.
    """
    x, y, d = beam

    o = grid[x][y]

    match o:
        case Object.HSPLITTER:  # "-"
            if d in VERTICAL:
                newd1, newd2 = Direction.EAST, Direction.WEST

                dx1, dy1 = newd1.delta()
                dx2, dy2 = newd2.delta()

                return [(x + dx1, y + dy1, newd1), (x + dx2, y + dy2, newd2)]
            else:
                dx, dy = d.delta()
                return [(x + dx, y + dy, d)]
        case Object.VSPLITTER:  # "|"
            if d in HORIZONTAL:
                newd1, newd2 = Direction.NORTH, Direction.SOUTH

                dx1, dy1 = newd1.delta()
                dx2, dy2 = newd2.delta()

                return [(x + dx1, y + dy1, newd1), (x + dx2, y + dy2, newd2)]
            else:
                dx, dy = d.delta()
                return [(x + dx, y + dy, d)]
        case Object.BMIRROR:  # "\"
            match d:
                case Direction.NORTH:
                    newd = Direction.WEST
                case Direction.WEST:
                    newd = Direction.NORTH
                case Direction.EAST:
                    newd = Direction.SOUTH
                case Direction.SOUTH:
                    newd = Direction.EAST
                case _:
                    raise ValueError(f"Invalid direction {d}")
            dx, dy = newd.delta()
            return [(x + dx, y + dy, newd)]
        case Object.FMIRROR:  # "/"
            match d:
                case Direction.NORTH:
                    newd = Direction.EAST
                case Direction.WEST:
                    newd = Direction.SOUTH
                case Direction.EAST:
                    newd = Direction.NORTH
                case Direction.SOUTH:
                    newd = Direction.WEST
                case _:
                    raise ValueError(f"Invalid direction {d}")
            dx, dy = newd.delta()
            return [(x + dx, y + dy, newd)]
        case _:  # empty space
            dx, dy = d.delta()
            return [(x + dx, y + dy, d)]


def energize(grid: ObjectGrid, start: Beam) -> int:
    """
    Return the energy from a grid.
    """
    nrow, ncol = len(grid), len(grid[0])

    q: deque[Beam] = deque()

    # our visited set is beam's, which encode direction
    # if we've been on this mirror IN THIS WAY, don't repeat
    v: set[Beam] = set()

    # v2 represents if we've visited a cell
    v2: set[tuple[int, int]] = set()

    # for debugging, build a energy grid
    energy_grid: Grid = []
    for _ in range(len(grid)):
        s = []
        for _ in range(len(grid[0])):
            s.append(".")
        energy_grid.append(s)

    sx, sy, _ = start
    # ...should probably validate start position

    q.append(start)

    energy = 1
    energy_grid[sx][sy] = "#"
    v2.add((sx, sy))

    while q:
        beam = q.popleft()

        for neighbor in neighbors(grid, beam):
            x, y, _ = neighbor
            if x < 0 or y < 0 or x >= nrow or y >= ncol:
                continue

            if neighbor not in v:
                q.append(neighbor)
                v.add(beam)

                # light the beam! if not visited
                if (x, y) not in v2:
                    energy += 1
                    v2.add((x, y))

                    if energy_grid[x][y] == "#":
                        raise ValueError(f"Touched {x}, {y} twice!")

                    energy_grid[x][y] = "#"

    return energy


def solve1() -> int:
    """
    Do a kind of directed BFS with "beams".
    """
    grid = get_grid()
    return energize(grid, (0, 0, Direction.EAST))


def solve2() -> int:
    """
    Try every starting beam position.

    Don't even bother with the corners; if I'm wrong, I'm wrong...
    """
    grid = get_grid()
    nrow, ncol = len(grid), len(grid[0])

    max_energy = 0

    for i in range(0, nrow):
        max_energy = max(max_energy, energize(grid, (i, 0, Direction.EAST)))
        max_energy = max(max_energy, energize(grid, (i, ncol - 1, Direction.WEST)))

    for j in range(0, nrow):
        max_energy = max(max_energy, energize(grid, (0, j, Direction.SOUTH)))
        max_energy = max(max_energy, energize(grid, (nrow - 1, j, Direction.NORTH)))

    return max_energy


if __name__ == "__main__":
    print(solve1())
    print(solve2())

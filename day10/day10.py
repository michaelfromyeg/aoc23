"""
https://adventofcode.com/2023/day/10
"""
from __future__ import annotations

import pprint
from enum import Enum

from utils.read import read

DAY = 10

DEBUG = True
TEST = 1


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


def connects(self: Pipe, other: Pipe, direction: Direction) -> bool:
    """
    Check if two pipes connect in a direction.
    """
    if (
        self == Pipe.NS
        and direction == Direction.N
        and other in [Pipe.NS, Pipe.SE, Pipe.SW]
    ):
        return True

    return False


def solve1() -> int:
    """ """
    lines = read(DAY, TEST if DEBUG else 0)

    grid: list[list[Pipe]] = []
    for line in lines:
        row: list[Pipe] = []
        for c in line.strip():
            row.append(str2pipe(c))
        grid.append(row)

    if DEBUG:
        pprint.pprint(grid)

    return 0


def solve2() -> int:
    """ """
    lines = read(DAY, TEST if DEBUG else 0)

    return 0


if __name__ == "__main__":
    print(solve1())
    print(solve2())

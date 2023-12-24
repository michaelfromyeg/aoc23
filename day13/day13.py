"""
https://adventofcode.com/2023/day/13
"""
from __future__ import annotations

from enum import StrEnum
from math import floor

from utils.read import read

DEBUG = True
TEST = 1

DAY = 13


class Object(StrEnum):
    """
    An object in the map.
    """

    ASH = "."
    ROCKS = "#"

    def flip(self) -> Object:
        """
        Return the opposite of myself.
        """
        return Object.ROCKS if self._value_ == "." else Object.ASH

    def __str__(self) -> str:
        return self._value_

    def __repr__(self) -> str:
        return self._value_


Map = list[list[Object]]


def print_map(a_map: Map) -> None:
    """
    Print the map, nicely.
    """
    for row in a_map:
        print("".join(row))
    print()


def str2object(c: str) -> Object:
    """
    Return an object.
    """
    if len(c) != 1:
        raise ValueError("Objects are single characters.")

    match c:
        case Object.ASH:
            return Object.ASH
        case Object.ROCKS:
            return Object.ROCKS
        case _:
            raise ValueError(f"Invalid object {c}")


def reflects_row(a_map: Map, n: int, line: float) -> int:
    """
    Return floor(line) if reflects, else 0.
    """
    fline = floor(line)

    to_check = min(fline, n - fline)

    i = 1
    while i <= to_check:
        if a_map[fline - i] != a_map[fline + i - 1]:
            return 0

        i = i + 1

    return fline


def reflects_col(a_map: Map, n: int, line: float) -> int:
    """
    Return floor(line) if reflects, else 0.
    """
    fline = floor(line)

    to_check = min(fline, n - fline)

    i = 1
    while i <= to_check:
        for row in a_map:  # new, because column indexing sucks
            if row[fline - i] != row[fline + i - 1]:
                return 0

        i = i + 1

    return fline


def score(a_map: Map) -> tuple[int, int]:
    """
    Determine the reflection score of a map.

    (a) find a vertical reflection line;   count the number of columns to its left
    (b) find a horizontal reflection line; count the number of rows above it
    """

    n_col = len(a_map[0])
    col_score = 0

    n_row = len(a_map)
    row_score = 0

    row_indices = [i / 2.0 for i in range(1 + 2, n_row * 2, 2)]
    for i in row_indices:
        row_score = max(row_score, reflects_row(a_map, n_row, i))

    col_indices = [i / 2.0 for i in range(1 + 2, n_col * 2, 2)]
    for j in col_indices:
        col_score = max(col_score, reflects_col(a_map, n_col, j))

    return row_score, col_score


def get_maps() -> list[Map]:
    """
    Determine the maps.
    """
    lines = read(DAY, TEST if DEBUG else 0)
    lines_str = "".join(lines)

    maps: list[Map] = []

    for chunk in lines_str.split("\n\n"):
        a_map: Map = []
        for line in chunk.split("\n"):
            line = line.strip()
            if not line:
                continue

            row = [str2object(c) for c in line]
            a_map.append(row)
        maps.append(a_map)

    return maps


def solve1() -> int:
    """
    Determine the 'size' of x- and y- reflections in a 2D grid.
    """
    maps = get_maps()

    row_total = 0
    col_total = 0
    for a_map in maps:
        row_score, col_score = score(a_map)

        row_total += row_score
        col_total += col_score

    return 100 * row_total + col_total


def solve2() -> int:
    """
    Try smudging a mirror.

    Brute force, for now.
    """
    maps = get_maps()

    row_total = 0
    col_total = 0
    for a_map in maps[:1]:
        o_rs = o_cs = score(a_map)

        row_score, col_score = 0, 0
        for i, row in enumerate(a_map):
            for j, c in enumerate(row):
                a_map[i][j] = c.flip()

                rs, cs = score(a_map)
                if rs == o_rs and cs == o_cs:
                    continue

                print(f"Flipped ({i},{j}), got: {row_score}, {col_score}")

                row_score = max(rs, row_score)
                col_score = max(cs, col_score)

                a_map[i][j] = c

        row_total += row_score
        col_total += col_score

    return 100 * row_total + col_total


if __name__ == "__main__":
    print(solve1())
    print(solve2())

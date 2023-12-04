"""
https://adventofcode.com/2023/day/3

I'll cheat and treat the symbols as sparse, not actually building out the graph.

Hopefully this is OK for part 2...
"""
import pprint

from utils.read import read

DEBUG = False


def solve1() -> int:
    """
    Sum the part numbers.
    """
    lines = read(3, test=DEBUG)

    symbols: dict[tuple[int, int], str] = {}

    def is_adjacent(row, s_col, e_col) -> bool:
        for col in range(s_col, e_col):
            coordinates = [
                (row, col),
                # top, bottom
                (row + 1, col),
                (row - 1, col),
                # left, right
                (row, col + 1),
                (row, col - 1),
                # diagonals
                (row - 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col + 1),
                (row + 1, col - 1),
            ]

            if any(coordinate in symbols for coordinate in coordinates):
                return True
        return False

    # on the first pass, parse the symbols
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if not char.isnumeric() and char != "." and char != "\n":
                symbols[(row, col)] = char

    if DEBUG:
        pprint.pprint(symbols)

    rv = 0
    for row, line in enumerate(lines):
        idx = 0
        while idx < len(line):
            candidate = ""
            start_idx = idx

            while line[idx].isnumeric():
                candidate += line[idx]
                idx += 1

            if candidate != "":
                if is_adjacent(row, start_idx, idx):
                    rv += int(candidate)
                candidate = ""

            idx += 1
    return rv


def solve2() -> int:
    """
    Sum the gears.
    """
    lines = read(3, test=DEBUG)

    # now a map from position to values
    gears: dict[tuple[int, int], list[int]] = {}

    def check_adjacent(row, s_col, e_col, value) -> None:
        for col in range(s_col, e_col):
            coordinates = [
                # top, bottom
                (row + 1, col),
                (row - 1, col),
            ]

            if col == s_col:
                coordinates.extend(
                    [
                        (row, col - 1),
                        (row - 1, col - 1),
                        (row + 1, col - 1),
                    ]
                )
            if col == e_col - 1:
                coordinates.extend(
                    [
                        (row, col + 1),
                        (row - 1, col + 1),
                        (row + 1, col + 1),
                    ]
                )

            for coordinate in coordinates:
                if coordinate in gears:
                    gears[coordinate].append(value)

    # on the first pass, parse the gears
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "*":
                gears[(row, col)] = []

    # then, determine the gear adjacencies
    for row, line in enumerate(lines):
        idx = 0
        while idx < len(line):
            candidate = ""
            start_idx = idx

            while line[idx].isnumeric():
                candidate += line[idx]
                idx += 1

            if candidate != "":
                check_adjacent(row, start_idx, idx, int(candidate))
                candidate = ""

            idx += 1

    if DEBUG:
        pprint.pprint(gears)

    rv = 0
    for values in gears.values():
        if len(values) == 2:
            rv += values[0] * values[1]
    return rv


if __name__ == "__main__":
    print(solve1())
    print(solve2())

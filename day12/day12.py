"""
https://adventofcode.com/2023/day/12
"""
from utils.read import read

DEBUG = True
DAY = 12


def pad(s: str, longest: int) -> str:
    """
    Pad a string with spaces.
    """
    return s + (longest - len(s)) * " "


def get_arrangements(record: str, totals: list[int], longest: int) -> int:
    """
    Determine the number of arrangements of springs possible.

    The idea? Generate every possible permutation, check if valid; return true if valid.

    Finish if sum(totals) == 0; then check arrangement (accumulator?)
    """
    print(f"{pad(record, longest)}{totals}")

    return 0


def solve1() -> int:
    """
    Sum possible arrangements for damaged springs.

    Springs are always contiguous.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    longest = 0
    for line in lines:
        longest = max(longest, len(line))

    arrangements = 0
    for line in lines:
        raw_record, totals_str = line.strip().split(" ")

        totals = [int(total) for total in totals_str.split(",")]
        arrangements += get_arrangements(raw_record, totals, longest)

    return arrangements


def solve2() -> int:
    """ """
    lines = read(DAY, 1 if DEBUG else 0)

    return 0


if __name__ == "__main__":
    print(solve1())
    print(solve2())

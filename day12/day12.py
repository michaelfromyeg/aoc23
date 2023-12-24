"""
https://adventofcode.com/2023/day/12
"""
from utils.read import read

DEBUG = True
TEST = 1

DAY = 12


def pad(s: str, longest: int) -> str:
    """
    Pad a string with spaces.
    """
    return s + (longest - len(s)) * " "


def _get_arrangements(record: str, count: int, last_replaced: int = -1) -> list[str]:
    """
    Get all possible arrangements.

    It'd be nice if this wasn't recursive. Also, we could check validate in the base case...
    """
    if count == 0:
        return [record.replace("?", ".")]

    records = []
    for i in range(last_replaced + 1, len(record), 1):
        if record[i] == "?":
            new_record = record[:i] + "#" + record[i + 1 :]
            records.extend(_get_arrangements(new_record, count - 1, i))

    return records


def _validate(arrangement: str, totals: list[int]) -> bool:
    """
    Determine if a suggested arrangement is valid.
    """
    n = len(arrangement)

    i = 0
    ti = 0

    while i < n:
        size = 0

        while i < n and arrangement[i] == "#":
            size += 1
            i += 1

        if size == 0:
            i += 1
            continue

        if size != totals[ti]:
            return False

        i += 1
        ti += 1

    return ti == len(totals)


def get_arrangements(record: str, totals: list[int], longest: int) -> int:
    """
    Determine the number of arrangements of springs possible.

    The idea? Generate every possible permutation, check if valid; return true if valid.

    Finish if sum(totals) == 0; then check arrangement (accumulator?)
    """
    if DEBUG:
        print(f"{pad(record, longest)}{totals}")

    grand_total = sum(totals)
    total_to_insert = grand_total - len([c for c in record if c == "#"])

    arrangements = _get_arrangements(record, total_to_insert)

    valid_arrangements = len(
        [arrangement for arrangement in arrangements if _validate(arrangement, totals)]
    )

    return valid_arrangements


def solve1() -> int:
    """
    Sum possible arrangements for damaged springs.

    Springs are always contiguous.
    """
    lines = read(DAY, TEST if DEBUG else 0)

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
    """
    Multiply the length of the string times 5.
    """
    lines = read(DAY, TEST if DEBUG else 0)

    longest = 0
    for line in lines:
        longest = max(longest, len(line))

    arrangements = 0
    for line in lines:
        raw_record, totals_str = line.strip().split(" ")

        new_raw_record = raw_record * 5

        totals = [int(total) for total in totals_str.split(",")]
        new_totals = totals * 5

        print(new_raw_record, new_totals)

        # TODO(michaelfromyeg): process the new arrangement
        arrangements += get_arrangements(new_raw_record, new_totals, longest)

    return arrangements


if __name__ == "__main__":
    print(solve1())
    # print(solve2())

"""
Parse a line into its digits, represented as numbers or written in English.
"""
digits1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

digits2 = digits1 + [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

digits2_map: dict[str, int] = {
    "1": 1,
    "one": 1,
    "2": 2,
    "two": 2,
    "3": 3,
    "three": 3,
    "4": 4,
    "four": 4,
    "5": 5,
    "five": 5,
    "6": 6,
    "six": 6,
    "7": 7,
    "seven": 7,
    "8": 8,
    "eight": 8,
    "9": 9,
    "nine": 9,
}


def read() -> list[str]:
    """
    Read the puzzle input.
    """
    with open("day1/input.txt") as f:
        lines = f.readlines()
        return lines


def solve1():
    """
    Parse a number from a string.
    """
    lines = read()

    rv = 0
    for line in lines:
        # looks like two loops, but really worst-case O(len(line)) together
        for c in line:
            if c in digits1:
                rv += int(c) * 10
                break

        for c in reversed(line):
            if c in digits1:
                rv += int(c)
                break
    return rv


def solve2():
    """
    Parse numbers potentially written in English.
    """

    def get_digits(line: str) -> list[int]:
        digits: list[int] = []
        idx = 0

        while idx < len(line):
            for digit in digits2:
                if line[idx : idx + len(digit)] == digit:
                    digits.append(digits2_map[digit])
                    break
            # there's some crappy edge cases to deal with
            # like "6oneighthlf" => [6, 1, 8]...
            # so we can't increment idx by len(digit)
            idx = idx + 1

        return digits

    lines = read()

    rv = 0
    for line in lines:
        digits = get_digits(line)
        rv += digits[0] * 10 + digits[-1]
    return rv


if __name__ == "__main__":
    rv1 = solve1()
    print(rv1)

    rv2 = solve2()
    print(rv2)

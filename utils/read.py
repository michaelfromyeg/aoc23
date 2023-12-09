"""
Helper methods for reading input.
"""


def read(day: int, test: int = 0) -> list[str]:
    """
    Read a file input into lines.
    """
    with open(f"day{day}/{f"test{test}" if test > 0 else "input"}.txt", encoding="utf-8") as f:
        lines = f.readlines()
        return lines

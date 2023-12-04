"""
Helper methods for reading input.
"""


def read(day: int, test: bool = False) -> list[str]:
    """
    Read a file input into lines.
    """
    with open(f"day{day}/{"test" if test else "input"}.txt", encoding="utf-8") as f:
        lines = f.readlines()
        return lines

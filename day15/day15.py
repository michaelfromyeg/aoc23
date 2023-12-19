"""
https://adventofcode.com/2023/day/15
"""
from dataclasses import dataclass

from utils.read import read

DEBUG = False
TEST = 1

DAY = 15

BOXES = 256


@dataclass
class Lens:
    """
    A lens in the box.
    """

    label: str
    value: int


@dataclass
class Box:
    """
    A box, with some lenses.
    """

    lenses: list[Lens]

    def remove(self, label: str) -> None:
        """
        Remove a label if present.
        """
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)

    def insert(self, label: str, value: int) -> None:
        """
        Insert a lens into the box.
        """
        for lens in self.lenses:
            if lens.label == label:
                lens.value = value
                return None

        self.lenses.append(Lens(label, value))


def fake_hash(s: str) -> int:
    """
    Process the string.
    """
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


def solve1() -> int:
    """
    Do the "HASH" algorithm.
    """
    lines = read(DAY, TEST if DEBUG else 0)

    values = lines[0].strip().split(",")

    current_value = 0
    for value in values:
        current_value += fake_hash(value)

    return current_value


def solve2() -> int:
    """ """
    lines = read(DAY, 1 if DEBUG else 0)

    values = lines[0].strip().split(",")

    boxes = [Box([]) for _ in range(BOXES)]

    for value in values:
        if "-" in value:
            label = value[:-1]
            box_number = fake_hash(label)

            boxes[box_number].remove(label)
        else:
            label, value = value.split("=")
            box_number = fake_hash(label)

            boxes[box_number].insert(label, int(value))

    # print non-empty boxes
    if DEBUG:
        for i, box in enumerate(boxes):
            if len(box.lenses) > 0:
                print(f"box={i}, {box}")

    focusing_power = 0
    for box_i, box in enumerate(boxes):
        for lens_i, lens in enumerate(box.lenses):
            focusing_power += (box_i + 1) * (lens_i + 1) * (lens.value)
    return focusing_power


if __name__ == "__main__":
    print(solve1())
    print(solve2())

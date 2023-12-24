"""
https://adventofcode.com/2023/day/24
"""
import itertools
from dataclasses import dataclass

import numpy as np

from utils.read import read

DEBUG = True
DAY = 24

GRID_MIN = 7 if DEBUG else 200000000000000
GRID_MAX = 24 if DEBUG else 400000000000000

Position = tuple[int, int, int]
Speed = tuple[int, int, int]


@dataclass
class Hailstone:
    """
    A hailstone, with position and speed.
    """

    pos: Position
    spd: Speed


def parse_hailstone(line: str) -> Hailstone:
    """
    e.g., 19, 13, 30 @ -2,  1, -2
    """
    pos_str, spd_str = line.split("@")

    pos_x, pos_y, pos_z = pos_str.strip().split(",")
    pos: Position = (int(pos_x.strip()), int(pos_y.strip()), int(pos_z.strip()))

    spd_x, spd_y, spd_z = spd_str.strip().split(",")
    spd: Speed = (int(spd_x.strip()), int(spd_y.strip()), int(spd_z.strip()))

    return Hailstone(pos, spd)


def intersect(h0: Hailstone, h1: Hailstone) -> bool:
    """
    Will these two hailstones intersect within [GRID_MIN, GRID_MAX]?

    Set a linear equation

    Ax = B

    Check if x is within the target region

    Take
    A: (19,13) @ (-2,1)
    B: (18,19) @ (-1,-1)

    x_1(t) = 19-2t, x_2(t) = 18-t
    y_1(t) = 13+t,  y_2(t) = 19-t

    x_1 = x_2
    19-2t = 18-t
    t=1

    y_1 = y_2
    13+t = 19-t
    2t=6, t=3
    """
    if True or DEBUG:
        print("A", h0)
        print("B", h1)

    h0_x, h0_y, _ = h0.pos
    h0_dx, h0_dy, _ = h0.spd

    h1_x, h1_y, _ = h1.pos
    h1_dx, h1_dy, _ = h1.spd

    if h0_dx == h1_dx and h0_dy == h1_dy:
        if DEBUG:
            print("No relative motion")
        return False

    coeffs = np.array([[h0_dx - h1_dx, 0], [0, h0_dy - h1_dy]])
    consts = np.array([h1_x - h0_x, h1_y - h0_y])

    # TODO(michaelfromyeg): handle 0 rows? (i.e., same dx, dy)
    non_zero_rows = ~np.all(coeffs == 0, axis=1)
    print(non_zero_rows)

    filtered_coeffs = coeffs[non_zero_rows, :]
    filtered_consts = consts[non_zero_rows]

    if filtered_coeffs.shape[0] == 0:
        return False

    try:
        print(filtered_coeffs, filtered_consts)
        t = np.linalg.solve(filtered_coeffs, filtered_consts)
    except np.linalg.LinAlgError:
        if DEBUG:
            print("No solution...?")
        return False

    if t[0] < 0 or t[1] < 0:
        if DEBUG:
            print("Negative time")
        return False

    x = h0_x + h0_dx * t[0]
    y = h0_y + h0_dy * t[0]

    if x > GRID_MAX or x < GRID_MIN or y > GRID_MAX or y < GRID_MIN:
        if DEBUG:
            print("Outside region")
        return False

    if True or DEBUG:
        print(f"{t[0]=}, {x=}, {y=}")

    return True


def solve1() -> int:
    """
    Christmas Eve.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    hailstones: list[Hailstone] = []
    for line in lines:
        hailstones.append(parse_hailstone(line.strip()))

    # "solve" all pairs of hailstones
    count = 0
    for pair in itertools.combinations(hailstones, r=2):
        if intersect(*pair):
            count += 1
        print()

    return count


def solve2() -> int:
    """ """
    lines = read(DAY, 1 if DEBUG else 0)

    return 0


if __name__ == "__main__":
    print(solve1())
    print(solve2())

"""
https://adventofcode.com/2023/day/6
"""
import math
import re
from dataclasses import dataclass

from utils.read import read

DEBUG = False
DAY = 6


@dataclass
class Race:
    """
    A race object.
    """

    # the maximum time of the race
    time: int

    # the current maximum distance
    dist: int


def solve_for_t_given_f(f_t: float, T: float) -> tuple[float, float] | None:
    """
    An overtuned quadratic solver.
    """
    a = -1
    b = T
    c = -f_t

    discriminant = b**2 - 4 * a * c

    if discriminant >= 0:
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return t1, t2
    else:
        return None


def solve1() -> int:
    """
    Determine the product of your winning ways.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    time_strs = re.sub(r"\s+", " ", lines[0]).strip().split(" ")[1:]
    distance_strs = re.sub(r"\s+", " ", lines[1]).strip().split(" ")[1:]

    races: list[Race] = []
    for time_str, distance_str in zip(time_strs, distance_strs):
        races.append(Race(int(time_str), int(distance_str)))

    # something about this problem feels like the binomial distribution
    # in the example for the 7 millisecond race, the times are

    # f(t) = total distance where
    # t is the time held
    # with a speed of 1mm/ms
    # so f(t) = t * (7 - t)
    # or generally, f(t) = t * (T - t)

    # f(0) = f(7) = 0
    # f(1) = f(6) = 6
    # f(2) = f(5) = 10
    # f(3) = f(4) = 12

    # pretty pattern :-)

    # to find the number of numbers that beat maximum
    # solve f(t) = D where D is the current record for t

    # count the number of integers between the bounds

    # by the quadratic formula
    # t = -T +/- sqrt(T^2) / -2

    print(races)

    ways_prod = 1
    for race in races:
        roots_or_none = solve_for_t_given_f(race.dist, race.time)

        if roots_or_none is None:
            raise ValueError("Given current maximum distance achieved is impossible!")

        lr, rr = roots_or_none

        # looks like a total hack, works; bad when we get integers as roots
        ways_prod *= len(range(math.ceil(lr + 0.01), math.floor(rr - 0.01) + 1))

    return ways_prod


def solve2() -> int:
    """
    Uh-oh. Bad kerning.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    time_strs = re.sub(r"\s+", " ", lines[0]).strip().split(" ")[1:]
    distance_strs = re.sub(r"\s+", " ", lines[1]).strip().split(" ")[1:]

    time_str = ""
    distance_str = ""
    for a_time_str, a_distance_str in zip(time_strs, distance_strs):
        time_str += a_time_str
        distance_str += a_distance_str

    super_race = Race(int(time_str), int(distance_str))

    roots_or_none = solve_for_t_given_f(super_race.dist, super_race.time)

    if roots_or_none is None:
        raise ValueError("Given current maximum distance achieved is impossible!")

    lr, rr = roots_or_none

    # looks like a total hack, works; bad when we get integers as roots
    ways = len(range(math.ceil(lr + 0.01), math.floor(rr - 0.01) + 1))

    return ways


if __name__ == "__main__":
    print(solve1())
    print(solve2())

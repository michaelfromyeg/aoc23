"""
https://adventofcode.com/2023/day/8
"""
import math
from dataclasses import dataclass
from enum import Enum

from utils.read import read

DEBUG = False
DAY = 8


class Step(Enum):
    """
    A step down the graph.
    """

    L = 0
    R = 1


@dataclass
class Node:
    """
    A node in the graph.
    """

    value: str

    ln: str
    rn: str

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Node):
            raise ValueError("Cannot compare with non-Node")

        return self.value == __value.value


def char2step(c: str) -> Step:
    """
    Convert a character to a step type.
    """
    if len(c) != 1:
        raise ValueError(f"{c} is not a character")

    match c:
        case "L":
            return Step.L
        case "R":
            return Step.R
        case _:
            raise ValueError(f"Invalid step {c}")


def parse_node(line: str) -> Node:
    """
    Turn a line into a Node.
    """
    value, children = line.split("=")

    value = value.strip()
    ln, rn = children.strip()[1:-1].split(",")

    return Node(value, ln.strip(), rn.strip())


def parse() -> tuple[list[Step], dict[str, Node]]:
    """
    Get the steps and node map.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    steps_str = lines[0].strip()
    steps: list[Step] = []

    for c in steps_str:
        steps.append(char2step(c))

    nodes: dict[str, Node] = {}
    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue

        node = parse_node(line)
        nodes[node.value] = node

    return steps, nodes


def solve1() -> int:
    """
    Determine the number of steps to reach z.
    """
    steps, nodes = parse()

    step_idx, step_n = 0, len(steps)

    cur = nodes["AAA"]
    tgt = nodes["ZZZ"]

    count = 0
    while cur != tgt:
        step = steps[step_idx]

        cur = nodes[cur.ln] if step == Step.L else nodes[cur.rn]

        count += 1
        step_idx = (step_idx + 1) % step_n

    return count


def lcm(nums: list[int]) -> int:
    """
    Get the lowest common multiple.
    """

    def lcm_of_two(a, b):
        return abs(a * b) // math.gcd(a, b)

    current_lcm = 1
    for num in nums:
        current_lcm = lcm_of_two(current_lcm, num)

    return current_lcm


def solve2() -> int:
    """
    Take many steps at the same time.

    The trick? I use LCM.

    I think this was a bit lucky since what if a path has multiple Zs? Like...

    A, B, Z, Z

    I only consider it's multiples of 3 -- maybe I should add all its possible Zs before looping
    """
    steps, nodes = parse()

    step_idx, step_n = 0, len(steps)

    curs: list[Node] = []
    for key, node in nodes.items():
        if key[-1] == "A":
            curs.append(node)

    count = 0
    zs: list[int] = []
    for cur in curs:
        count = 0
        step_idx = 0

        # count for this value
        new_cur = cur
        while new_cur.value[-1] != "Z":
            step = steps[step_idx]

            new_cur = nodes[new_cur.ln] if step == Step.L else nodes[new_cur.rn]

            count += 1
            step_idx = (step_idx + 1) % step_n

        zs.append(count)

    return lcm(zs)


if __name__ == "__main__":
    print(solve1())
    print(solve2())

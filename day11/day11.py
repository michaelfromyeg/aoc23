"""
https://adventofcode.com/2023/day/11
"""
import pprint
from collections import deque
from dataclasses import dataclass

from utils.read import read

DEBUG = False
DAY = 11


def pretty_print_2d_array(arr: list[list[int]]) -> None:
    """
    Pretty print my distance grid.
    """
    if not arr:
        return None

    # Find the maximum value in the array for determining padding
    max_value = max(max(row) for row in arr if row)
    padding = len(str(max_value))

    # Print each row with proper formatting
    for row in arr:
        formatted_row = " ".join(f"{num:0{padding}d}" for num in row)
        print(formatted_row)


@dataclass
class Node:
    """
    A node in the galaxy.
    """

    x: int
    y: int

    galaxy: bool
    cost: int  # 1 or 2, depending on if the space expands

    def __repr__(self) -> str:
        # return str(self.cost)
        return "#" if self.galaxy else "."

    def __str__(self) -> str:
        # return str(self.cost)
        return "#" if self.galaxy else "."

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def neighbors(space: list[list[Node]], node: Node) -> list[Node]:
    """
    Get the neighbors of a node.
    """
    ns: list[Node] = []

    if node.x > 0:
        ns.append(space[node.x - 1][node.y])
    if node.y > 0:
        ns.append(space[node.x][node.y - 1])
    if node.x < len(space) - 1:
        ns.append(space[node.x + 1][node.y])
    if node.y < len(space[0]) - 1:
        ns.append(space[node.x][node.y + 1])

    return ns


def bfs(space: list[list[Node]], s: Node) -> list[list[int]]:
    """
    Perform a simple BFS traversal. Returns distance map from s.

    NOTE: we don't have to use Dijkstra's here because EVERY shortest path would have to cross the empty row or column. There's no way 'around.'

    So, we can add the node's cost. This doesn't work if either of the two properties does not old

    - there exists space[i_1][j_1], space[i_2][j_2] st i_1 == i_2 and their costs are not equal
    - there exists space[i_1][j_1], space[i_2][j_2] st j_1 == j_2 and their costs are not equal
    """
    q: deque[Node] = deque()
    v: set[Node] = set()

    q.append(s)

    d: list[list[int]] = [[0 for _ in range(len(space[0]))] for _ in range(len(space))]

    while q:
        node = q.popleft()

        for neighbor in neighbors(space, node):
            if neighbor not in v:
                v.add(neighbor)
                q.append(neighbor)

                d[neighbor.x][neighbor.y] = d[node.x][node.y] + node.cost

    return d


def solve1(cost: int = 2) -> int:
    """
    Shortest paths between all planets in a galaxy.

    Empty rows, columns "cost" double.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    space: list[list[Node]] = []

    galaxies: list[Node] = []

    for i, line in enumerate(lines):
        line = line.strip()

        space_row: list[Node] = []

        for j, c in enumerate(line):
            if c == "#":
                g = Node(i, j, True, 1)
                space_row.append(g)
                galaxies.append(g)
            else:
                space_row.append(Node(i, j, False, 1))
        space.append(space_row)

    # update the row costs
    for row in space:
        if not any([node.galaxy for node in row]):
            for node in row:
                node.cost = cost

    # update the column costs
    for index in range(len(space[0])):
        col = [space[i][index] for i in range(len(space))]

        if not any([node.galaxy for node in col]):
            for node in col:
                node.cost = cost

    if not galaxies:
        raise ValueError(f"No galaxies found in space, {space}")

    if DEBUG:
        pprint.pprint(f"s={galaxies[0]} @ ({galaxies[0].x}, {galaxies[0].y})")
        pprint.pprint(space)

    total = 0
    for i in range(0, len(galaxies) - 1, 1):
        distances = bfs(space, galaxies[i])

        for j in range(i + 1, len(galaxies), 1):
            other_galaxy = galaxies[j]
            total += distances[other_galaxy.x][other_galaxy.y]

    return total


def solve2() -> int:
    """
    This was fortunately easy.
    """
    return solve1(100 if DEBUG else 10**6)


if __name__ == "__main__":
    print(solve1())
    print(solve2())

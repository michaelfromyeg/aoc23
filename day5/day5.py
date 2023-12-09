"""
"""
from dataclasses import dataclass

from utils.read import read

DEBUG = True


@dataclass
class Range:
    """
    A mapping range.
    """

    src_start: int
    dst_start: int

    length: int


@dataclass
class XYMap:
    """
    A map from source-to-destination, for ranges.
    """

    src: str
    dst: str

    ranges: list[Range]


def parse_seeds(line: str) -> list[int]:
    """
    Get seeds from the (first) line.
    """
    seeds_str = line.split(" ")[1:]
    return [int(seed_str.strip()) for seed_str in seeds_str]


def parse_src_dst(line: str) -> tuple[str, str]:
    """
    Get src-to-dst values.
    """
    src, _, dstish = line.split("-")
    dst, _ = dstish.split(" ")

    return src.strip(), dst.strip()


def parse_ranges(lines: list[str]) -> list[Range]:
    """
    Parse ranges.
    """
    ranges: list[Range] = []

    for line in lines:
        dst_start, src_start, length = line.split(" ")
        ranges.append(
            Range(
                src_start=int(src_start), dst_start=int(dst_start), length=int(length)
            )
        )

    return ranges


def parse_map(chunk: str) -> XYMap:
    """
    Get a map from a chunk.
    """
    values = [s.strip() for s in chunk.split("\n\n")]

    src, dst = parse_src_dst(values[0])
    ranges = parse_ranges(values[1:])

    return XYMap(src, dst, ranges)


def do_maps(seed: int, maps: list[XYMap]) -> int:
    """
    Return a location.
    """
    curr_val = seed

    curr_key = "seed"
    trgt_key = "location"

    while curr_key != trgt_key:
        curr_map = None
        for a_map in maps:
            if a_map.src == curr_key:
                curr_map = a_map
                break

        if curr_map is None:
            raise ValueError(f"No map exists for {curr_key}")

        curr_range = None
        for a_range in curr_map.ranges:
            if curr_val in range(
                a_range.src_start, a_range.src_start + a_range.length + 1
            ):
                curr_range = a_range
                break

        if curr_range is not None:
            curr_val = curr_range.dst_start + (curr_val - curr_range.src_start)

        curr_key = curr_map.dst

    return curr_val


def solve1() -> int:
    """ """
    lines = read(5, 1 if DEBUG else 0)

    seeds = parse_seeds(lines[0])

    map_strs = "\n".join(lines[2:]).split("\n\n\n")
    maps = [parse_map(map_str) for map_str in map_strs]

    locations = [do_maps(seed, maps) for seed in seeds]

    return min(locations)


def do_maps2(seed_range: tuple[int, int], maps: list[XYMap]) -> int:
    """
    Return a location.

    TODO: https://chat.openai.com/share/ef68ce29-23f6-480c-96dd-4ade9c5bf67a
    """
    curr_val = seed_range

    curr_key = "seed"
    trgt_key = "location"

    while curr_key != trgt_key:
        curr_map = None
        for a_map in maps:
            if a_map.src == curr_key:
                curr_map = a_map
                break

        if curr_map is None:
            raise ValueError(f"No map exists for {curr_key}")

        curr_range = None
        for a_range in curr_map.ranges:
            if curr_val in range(
                a_range.src_start, a_range.src_start + a_range.length + 1
            ):
                curr_range = a_range
                break

        if curr_range is not None:
            curr_val = curr_range.dst_start + (curr_val - curr_range.src_start)

        curr_key = curr_map.dst

    return curr_val


def get_new_seeds(seeds: list[int]) -> list[tuple[int, int]]:
    """ """
    seed_ranges: list[tuple[int, int]] = []

    idx = 0
    while idx < len(seeds):
        seed_ranges.append((seeds[idx], seeds[idx + 1]))
        idx += 2

    return seed_ranges


def solve2() -> int:
    """ """
    lines = read(5, 1 if DEBUG else 0)

    seeds = parse_seeds(lines[0])
    new_seeds = get_new_seeds(seeds)

    map_strs = "\n".join(lines[2:]).split("\n\n\n")
    maps = [parse_map(map_str) for map_str in map_strs]

    locations = [do_maps2(seed, maps) for seed in new_seeds]

    idx = 0
    while idx < len(locations):
        print(new_seeds[idx], locations[idx])
        idx += 1

    return min(locations)


if __name__ == "__main__":
    print(solve1())
    print(solve2())

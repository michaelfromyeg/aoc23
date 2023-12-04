"""
https://adventofcode.com/2023/day/2
"""
from dataclasses import dataclass

from utils.read import read


@dataclass
class Draw:
    """
    A draw of cubes.
    """

    r: int
    g: int
    b: int


@dataclass
class Game:
    """
    A game; a collection of draws.
    """

    game_id: int
    draws: list[Draw]


R, G, B = 12, 13, 14


def parse_games() -> list[Game]:
    """
    Parse the games.
    """
    lines = read(2)
    games: list[Game] = []

    for line in lines:
        game_string, draws_string = line.split(":")

        game_string = game_string.strip()
        _, game_id = game_string.split(" ")

        draws_string = draws_string.strip()
        draws: list[Draw] = []

        for draw_string in draws_string.split(";"):
            draw_string = draw_string.strip()

            values = draw_string.split(",")

            r, g, b = 0, 0, 0
            for value in values:
                value = value.strip()

                number_str, color = value.split(" ")
                number = int(number_str)

                match color:
                    case "red":
                        r = number
                    case "blue":
                        b = number
                    case "green":
                        g = number

            draws.append(Draw(r, g, b))

        games.append(Game(int(game_id), draws))

    return games


def solve1() -> int:
    """
    Cube conundrum.
    """

    def is_valid(game: Game) -> bool:
        return all(draw.r <= R and draw.g <= G and draw.b <= B for draw in game.draws)

    rv = 0
    for game in parse_games():
        if is_valid(game):
            rv += game.game_id

    return rv


def solve2() -> int:
    """
    Now, get the minimum number of cubes required.
    """

    def power(game: Game) -> int:
        """
        Get the minimum cubes for the game.
        """
        r, g, b = 0, 0, 0

        for draw in game.draws:
            r = max(r, draw.r)
            g = max(g, draw.g)
            b = max(b, draw.b)

        return r * g * b

    rv = 0
    for game in parse_games():
        rv += power(game)
    return rv


if __name__ == "__main__":
    print(solve1())
    print(solve2())

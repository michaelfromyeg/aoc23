"""
https://adventofcode.com/2023/day/4
"""
import pprint
from dataclasses import dataclass

from utils.read import read

DEBUG = False


@dataclass
class Card:
    """
    A scratchcard.
    """

    card_id: int

    wins: list[int]
    mine: list[int]


def parse_card(line: str) -> Card:
    """
    Get a card from a line.

    e.g., Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    """

    def remove_many_space(s: str) -> str:
        """
        Total hack. Wouldn't extend to N spaces, but whatever.
        """
        return s.replace("   ", " ").replace("  ", " ")

    card_info, card_details = line.split(":")

    card_id = int(remove_many_space(card_info).split(" ")[1].strip())

    wins_str, mine_str = card_details.split(" | ")

    wins = [int(number) for number in remove_many_space(wins_str.strip()).split(" ")]
    mine = [int(number) for number in remove_many_space(mine_str.strip()).split(" ")]

    return Card(card_id, mine=mine, wins=wins)


def parse_cards() -> list[Card]:
    """
    Turn the raw input into `Cards`.
    """
    lines = read(4, DEBUG)

    cards: list[Card] = []
    for line in lines:
        cards.append(parse_card(line))

    if DEBUG:
        pprint.pprint(cards)

    return cards


def solve1() -> int:
    """
    Scratch cards.
    """
    cards = parse_cards()

    rv = 0
    for card in cards:
        count = -1

        for my_number in card.mine:
            if my_number in card.wins:
                count += 1

        if count >= 0:
            rv += 2**count

    return rv


def solve2() -> int:
    """
    Scratch cards.
    """
    cards = parse_cards()

    # card_id, card_value
    card_map: dict[int, int] = {}

    for card in reversed(cards):
        count = -1
        for my_number in card.mine:
            if my_number in card.wins:
                count += 1

        # start with this card
        card_count = 1

        for card_id in range(card.card_id + 1, card.card_id + 1 + count + 1):
            card_count += card_map[card_id]

        card_map[card.card_id] = card_count

    return sum(card_map.values())


if __name__ == "__main__":
    print(solve1())
    print(solve2())

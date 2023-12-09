"""
https://adventofcode.com/2023/day/7
"""
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum

from utils.read import read

DEBUG = False
DAY = 7

card_types_str = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
card_types_wildcard_str = [
    "J",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "Q",
    "K",
    "A",
]


def card_sort_key(card: str, wildcard: bool = False):
    """
    Helper to get the value of a card.
    """
    if len(card) != 1:
        raise ValueError(f"{card} is not a valid card; incorrect length")
    return (
        card_types_wildcard_str.index(card) if wildcard else card_types_str.index(card)
    )


class HandType(IntEnum):
    """
    Possible hand types, ordered.
    """

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def merge_wildcard(counter: Counter) -> Counter:
    """
    Merge the jacks optimally in the counter.

    What progressions can I make?

    high card -> one pair
    A234J ... AA234

    one pair, no J -> trips
    AA23J ... AAA23

    one pair, J -> trips
    A23JJ ...AAA23

    two pair, no J -> full house
    AA22J ... AAA22

    two pair, J -> four of a kind
    AA2JJ ... AAAA2

    trips, no J -> four of a kind
    AAA2J ... AAAA2

    trips, J -> four of a kind
    A2JJJ ... AAAA2

    full house, no J -> full house
    AAA22 ... AAA22

    full house, J -> five of a kind
    AAAJJ ... AAAAA
    JJJAA ... AAAAA

    four of a kind, J -> five of a kind
    AJJJJ ... AAAAA

    four of a kind, no J -> five of a kind
    AAAAJ ... AAAAA

    five of a kind, J -> five of a kind
    JJJJJ ... JJJJJ

    five of a kind, no J

    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6
    """
    n_jacks = counter["J"]
    if n_jacks == 0 or n_jacks == 5:
        return counter

    before_counter = counter.copy()

    # Add the jacks to the most frequent letter
    del counter["J"]

    mc_key, mc_val = counter.most_common(1)[0]
    counter[mc_key] = mc_val + n_jacks

    if DEBUG:
        print("before", before_counter)
        print("after", counter)

    return counter


@dataclass
class Hand:
    """
    A hand and it's bid amount.
    """

    cards: str
    bid: int
    wildcard: bool = False

    def _best_type_and_ordered_cards(self) -> HandType:
        """
        Get the best hand and sorted deck for a hand,
        """
        counts = Counter(self.cards)
        if self.wildcard:
            counts = merge_wildcard(counts)

        sorted_counts = sorted(counts.values(), reverse=True)

        match sorted_counts:
            case [5]:
                return HandType.FIVE_OF_A_KIND
            case [4, 1]:
                return HandType.FOUR_OF_A_KIND
            case [3, 2]:
                return HandType.FULL_HOUSE
            case [3, 1, 1]:
                return HandType.THREE_OF_A_KIND
            case [2, 2, 1]:
                return HandType.TWO_PAIR
            case [2, 1, 1, 1]:
                return HandType.ONE_PAIR
            case [1, 1, 1, 1, 1]:
                return HandType.HIGH_CARD
            case _:
                raise ValueError(f"Impossible counts found: {sorted_counts}")

    def __lt__(self, other):
        """
        Is one hand less than another?
        """
        my_hand, my_cards = self._best_type_and_ordered_cards(), [
            card_sort_key(card, self.wildcard) for card in self.cards
        ] if self.wildcard else [card_sort_key(card) for card in self.cards]
        ot_hand, ot_cards = other._best_type_and_ordered_cards(), [
            card_sort_key(card, self.wildcard) for card in other.cards
        ]

        if my_hand == ot_hand:
            for my_card, ot_card in zip(my_cards, ot_cards):
                if my_card == ot_card:
                    continue
                else:
                    return my_card < ot_card
        else:
            return my_hand < ot_hand

        # if completely equal, less than is false
        return False


def get_winnings(hands: list[Hand]) -> int:
    """
    Determine the winnings of a list of hands.
    """
    n = len(hands)
    total = 0

    for i, hand in enumerate(hands):
        total += (n - i) * hand.bid

    return total


def solve1(wildcard: bool = False) -> int:
    """
    Determine the best hand, poker-ish.
    """
    lines = read(DAY, 1 if DEBUG else 0)

    hands: list[Hand] = []
    for line in lines:
        cards, bid_str = line.strip().split(" ")
        hands.append(Hand(cards, int(bid_str), wildcard))

    hands.sort(reverse=True)

    return get_winnings(hands)


def solve2() -> int:
    """
    Jacks become jokers.
    """
    return solve1(True)


if __name__ == "__main__":
    print(solve1())
    print(solve2())

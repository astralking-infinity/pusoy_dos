import math
from random import random
from collections import namedtuple
from functools import partial

from colorama import Fore, Back

Suit = namedtuple('Suit', ['name', 'rank', 'uni'])
diamonds = Suit('Diamonds', 1, b'\xE2\x99\xA6'.decode())
hearts = Suit('Hearts', 2, b'\xE2\x99\xA5'.decode())
spades = Suit('Spades', 3, b'\xE2\x99\xA0'.decode())
clubs = Suit('Clubs', 4, b'\xE2\x99\xA3'.decode())

SUIT = {'Diamonds': diamonds,
        'Hearts': hearts,
        'Spades': spades,
        'Clubs': clubs}

CARD_RANKS = ('3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace', '2')


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.suit!r}, {self.value!r})'

    def __str__(self):
        return f'{self.value} of {self.suit}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__

    # Suit ranking: lowest number is equivalent to highest ranking
    # Card values ranking (highest to lowest): 2-A-K-Q-J-10-9...3
    def __gt__(self, other):
        if self.value == other.value:
            return SUIT[self.suit].rank < SUIT[other.suit].rank  ## Test
        return CARD_RANKS.index(self.value) > CARD_RANKS.index(other.value)

    def show(self, display=True):
        if self.suit in ['Diamonds', 'Hearts']:
            fancy_display = f'{Fore.RED}{SUIT[self.suit].uni} {Fore.RESET}{self.value}'
        else:
            fancy_display = f'{Fore.BLACK}{Back.WHITE}{SUIT[self.suit].uni} {Back.RESET}{Fore.RESET}{self.value}'

        if display:
            print(fancy_display)
        else:
            return fancy_display


class Deck:
    """A standard 52-card deck."""

    def __init__(self):
        self._cards = []
        self.build()

    def __len__(self):
        return len(self._cards)

    def build(self):
        self._cards = []
        for suit in SUIT.keys():
            for value in CARD_RANKS:
                self._cards.append(Card(suit, value))
        self._cards.sort(key=partial(card_func_key, suit_priority=True))

    def shuffle(self):
        # Using Fisher-Yates modern shuffle algorithm
        for i in range(len(self._cards)-1, 0, -1):
            r = math.floor(random() * (i+1))
            self._cards[i], self._cards[r] = self._cards[r], self._cards[i]
        # Or just the standard random.shuffle()

    def _show_cards(self):
        for card in self._cards:
            card.show()

    def draw_card(self):
        return self._cards.pop()

    def not_empty(self):
        if self._cards:
            return True


class CardPlay:
    """Data class for cards played by the player."""

    five_card_group = {'Straight': 1,
                       'Flush': 2,
                       'Full house': 3,
                       'Four of a kind': 4,
                       'Straight flush': 5}

    def __init__(self, combotype, cards):
        self.combotype = combotype
        self.cards = cards
        self.category = combotype.lower() if combotype not in self.five_card_group \
                        else 'five-card'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.combotype!r}, {self.cards!r})'

    def __str__(self):
        cards_str = '-'.join(card.show(display=False) for card in self.cards)
        return f'{self.combotype} of {cards_str}'


# Sorting key for cards:
#   Sort cards by their value(by numerical or by rank) then suit rank by default.
def card_func_key(card, valueby='numerical', suit_priority=False):
    if valueby == 'rank':
        return (CARD_RANKS.index(card.value), -(SUIT[card.suit].rank))
    else:
        numerical = CARD_RANKS[11:] + CARD_RANKS[:11]
        if suit_priority:
            return (
                -(SUIT[card.suit].rank), numerical.index(card.value)
            )
        return (
            numerical.index(card.value), -(SUIT[card.suit].rank)
        )


# An extension of sorting key.
#   Count number of frequency of an item
def frequency_counter(card, group_cards=None, func=None, **kwargs):
    return [len(group_cards[card.value])] + list(func(card, **kwargs))


# Helper function for grouping cards according to value
def group_value(cards):
    value = {}
    for card in cards:
        value.setdefault(card.value, []).append(card)
    return value


if __name__ == '__main__':
    # Pusoy dos (Filipino Poker)
    # Rules:
    #   -> Suits ranking (from highest to lowest): 'Diamonds', 'Hearts', 'Spades', 'Clubs'
    #   -> Cards ranking: highest is '2 of Diamonds', Lowest card is '3 of Clubs'
    # Combinations:
    #   Pair: 2 cards with equal value
    #   Three of a kind: 3 cards with equal value
    #   Straight: 5 cards with consecutive value with different suits (Rank by highest single in each straight)
    #   Flush: 5 cards with same suit (Ranked by suits of each Flush)
    #   Full house: Combination of Three of a kind and a Pair (Ranked by Three of a kind used)
    #   Four of a kind: 4 cards with equal value plus a single card of any value (Ranked by four cards used)
    #   Straight flush: 5 cards with consecutive values and same suit

    from player import ActivePlayer, Player

    # Initialize deck
    deck = Deck()
    deck.shuffle()

    # Prepare players
    john = Player('John')
    jane = Player('Jane')
    jess = Player('Jess')
    june = Player('June')

    # players = [john, jane, jess, june]
    players = ActivePlayer(john, jane, jess, june)

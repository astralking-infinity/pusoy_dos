#!/usr/bin/python3.6

"""pusoy_dos.py

Pusoy Dos or Filipino Poker
"""

import math
import sys
from random import random
from collections import namedtuple
from functools import partial
from pprint import pprint

from colorama import Fore, Back

from player_nodes import ActivePlayer

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

discards = []
plays = []


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

    def show(self):
        if self.suit in ['Diamonds', 'Hearts']:
            print(f'{Fore.RED}{SUIT[self.suit].uni} {Fore.RESET}{self.value}')
        else:
            print(f'{Fore.BLACK}{Back.WHITE}{SUIT[self.suit].uni} {Back.RESET}{Fore.RESET}{self.value}')


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


class Player:
    # Combination = namedtuple('Combination', ['combotype', 'cards'])
    # Combination = CardPlay()
    count = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.count += 1

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'

    def draw(self, deck):
        if deck.not_empty():
            self.hand.append(deck.draw_card())

    def show_hand(self):
        for i, card in enumerate(self.hand):
            #print(f'{i+1:<2}', end=' ')
            card.show()

    def play(self, combotype, cards):
        cards = sorted(cards, key=partial(card_func_key, valueby='rank'))
        for card in cards:
            self.hand.pop(self.hand.index(card))
        return CardPlay(combotype, cards)

    def discard(self, card):
        if card in self.hand:
            self.hand.pop(self.hand.index(card))

    def sort_hand(self):
        self.hand.sort(key=card_func_key)


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


# Check if cards' combination is valid
def verify_combination(cards):
    for rule in (is_single,
                 is_pair,
                 is_three_of_a_kind,
                 is_straight_flush,
                 is_straight,
                 is_flush,
                 is_full_house,
                 is_four_of_a_kind):
        valid, name = rule(cards)
        if valid:
            return valid, name
    return False, None


def is_single(cards):
    return len(cards) == 1, 'Single'


def is_pair(cards):
    return len(cards) == 2 and cards[0].value == cards[1].value, 'Pair'


def is_three_of_a_kind(cards):
    return len(cards) == 3 and cards[0].value == cards[1].value == cards[2].value, 'Three of a kind'


def is_straight(cards):
    if len(cards) < 5:
        return False
    cards = sorted(cards, key=card_func_key)
    card_values = list(map(lambda c: c.value, cards))
    # If cards contains both King and Ace place the Ace at the end of card_values
    if 'King' in card_values and 'Ace' in card_values:
        card_values = card_values[1:] + card_values[:1]
    possible_straight = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    for i in range( len(possible_straight)-4 ):
        if card_values == possible_straight[i:i+5]:
            return True, 'Straight'
    return False, 'Straight'


def is_flush(cards):
    return len(cards) == 5 and all(card.suit==cards[0].suit for card in cards), 'Flush'


def is_full_house(cards):
    if len(cards) < 5:
        return False
    card_groups = {}
    for card in cards:
        card_groups.setdefault(card.value, []).append(card)
    return [2, 3] == sorted(map(len, card_groups.values())), 'Full house'


def is_four_of_a_kind(cards):
    if len(cards) < 5:
        return False
    card_groups = {}
    for card in cards:
        card_groups.setdefault(card.value, []).append(card)
    return [1, 4] == sorted(map(len, card_groups.values())), 'Four of a kind'


def is_straight_flush(cards):
    valid_straight, _ = is_straight(cards)
    valid_flush, _ = is_flush(cards)
    return len(cards) == 5 and valid_straight and valid_flush, 'Straight flush'


def is_higher(self, other):
        """Check higher card combination based on category they belong."""
        if self.category == other.category:
            if self.category != 'five-card':
                return self.cards[-1] > other.cards[-1]
            else:
                # Comparing two card combination with same type
                if self.combotype == other.combotype:
                    if self.combotype in ('Full house', 'Four of a kind', 'Straight'):
                        return self.cards[-1] > other.cards[-1]
                    else:  # self.combotype in ('Flush', 'Straight flush')
                        if self.cards[-1].suit == other.cards[-1].suit:
                            return self.cards[-1].value > other.cards[-1].value
                        return self.cards[-1].suit < other.cards[-1].suit
                    # elif self.combotype == 'Straight':
                    #     print('Not yet implemented.')
                    # elif self.combotype == 'Straight flush':
                    #     print('Not yet implemented.')
                else:
                    return CardPlay.five_card_group[self.combotype] > CardPlay.five_card_group[other.combotype]
        else:
            print(f"Invalid match up.")
            return False


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

    deck = Deck()
    deck.shuffle()

    john = Player('John')
    jane = Player('Jane')
    jess = Player('Jess')
    june = Player('June')

    # players = [john, jane, jess, june]
    players = ActivePlayer(john, jane, jess, june)

    # Distribute card for each player
    while deck.not_empty():
        players.next_turn().draw(deck)

    player = players.next_turn()
    print(player.name)
    player.show_hand()
    # for player in players:
    #     print(f"{player}")
    #     player.show_hand()
    #     print()

    # june.sort_hand()

    # Sample cards to test ranking of card combinations
    card1 = Card('Hearts', '2')
    card2 = Card('Spades', '2')
    sample_cards1 = [
        card1
    ]
    # valid, combotype = verify_combination(sample_cards)
    # plays.append(june.play(combotype, sample_cards))

    card3 = Card('Diamonds', '2')
    card4 = Card('Clubs', '2')
    sample_cards2 = [
        card4
    ]

    # pair1 = Player.Combination('Pair', sample_cards1)
    # pair2 = Player.Combination('Single', sample_cards2)
    # print(pair1 == pair2)
    # print(sample_cards1 == sample_cards2)
    #print(is_higher(pair1, pair2))

    # june.show_hand()

    # Sample play
    # card2 = Card('Hearts', '2')
    # my_discaard = [card2]
    # valid, combotype = verify_combination(my_play)
    # print(card2 > card1)

    # while True:
    #     for player in players:
    #         print(f"{player.name}'s turn.")
    #         player.sort_hand()
    #         player.show_hand()

    #         picked_cards = []
    #         while True and len(picked_cards) < 5:

    #             # try:
    #                 picked_card = input('Choose card to form a combination:(<suit> <value>): ').title()
    #                 if not picked_card:
    #                     continue

    #                 # Optional exit status for faster bug fixing.
    #                 if picked_card == 'Quit' or picked_card == 'Q':
    #                     sys.exit()
    #                 elif picked_card == 'Done' or picked_card == 'D':
    #                     break

    #                 suit, value = picked_card.split()

    #                 if suit not in SUIT.keys() or \
    #                         value not in (list(map(str, range(1, 11))) + list(HONOUR.values())):
    #                     print(f"Wrong input.")
    #                     continue

    #                 card = Card(suit, value)
    #                 if card not in player.hand:
    #                     print(f"You don't have the card, {card}")
    #                 elif card in picked_cards:
    #                     print(f'{card} is already picked. Choose another one.')
    #                 else:
    #                     picked_cards.append(card)
    #             # except:
    #             #     print('Invalid input format.')

    #         picked_cards = sorted(picked_cards, key=partial(card_func_key, valueby='rank'))
    #         valid, combotype = verify_combination(picked_cards)
    #         if valid:
    #             if plays:
    #                 if plays[-1].combotype == 'Single':
    #                     print('Singles combination battle.')
    #                     if picked_cards[0] > plays[-1].cards[0]:
    #                         pass
    #                 # elif plays[-1][0] == 'Pair':
    #                 #     print('Pairs combination battle.')
    #                 # elif plays[-1][0] == 'Three of a kind':
    #                 #     print('Three of a kind combination battle.')
    #                 # else:
    #                 #     print('Five-card hand combination battle.')
    #             plays.append(player.play(combotype, picked_cards))
    #             pprint(plays)
    #             # player.show_hand()
    #         else:
    #             print('No valid combination found. Try again.')

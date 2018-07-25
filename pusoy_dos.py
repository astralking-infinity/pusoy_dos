#!/usr/bin/python3.6

"""pusoy_dos.py

Pusoy Dos or Filipino Poker
"""

import math
import sys
from random import random
from collections import namedtuple
from pprint import pprint

from colorama import Fore, Back

from player_nodes import ActivePlayer

Suit = namedtuple('Suit', ['name', 'rank', 'uni'])
diamonds = Suit('Diamonds', 1, b'\xE2\x99\xA6'.decode())
hearts = Suit('Hearts', 2, b'\xE2\x99\xA5'.decode())
spades = Suit('Spades', 3, b'\xE2\x99\xA0'.decode())
clubs = Suit('Clubs', 4, b'\xE2\x99\xA3'.decode())

SUITS = {'Diamonds': diamonds,
         'Hearts': hearts,
         'Spades': spades,
         'Clubs': clubs}
HONOURS = {'Jack': '11', 'Queen': '12', 'King': '13', 'Ace': '1'}

CARD_RANKS = ('3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace', '2')

discard_pile = []


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.suit!r}, {self.value!r})'

    def __str__(self):
        return f'{self.value} of {self.suit}'

    # Part which is quite confusing as without this method the class Player's discard method
    # won't return the result as expected.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__

    # Reverse comparison of greater than and less than so comparison of card suits match
    # the order of suit ranking where 1 would be the highest.
    # Card values ranking(highest to lowest): 2-A-K-Q-J-10-9...3
    def __gt__(self, other):
        if self.value == other.value:
            return SUITS[self.suit].rank < SUITS[other.suit].rank  ## Test
        return CARD_RANKS.index(self.value) > CARD_RANKS.index(other.value)

    def show(self, end='\n'):
        if self.suit in ['Diamonds', 'Hearts']:
            print(f'{Fore.RED}{SUITS[self.suit].uni} {Fore.RESET}{self.value}')
        else:
            print(f'{Fore.BLACK}{Back.WHITE}{SUITS[self.suit].uni} {Back.RESET}{Fore.RESET}{self.value}')


class Deck:

    def __init__(self):
        self._cards = []
        self.build()

    def __len__(self):
        return len(self._cards)

    def build(self):
        for suit in SUITS:
            for value in CARD_RANKS:
                self._cards.append(Card(suit, value))
        self._cards.sort(key=card_func_key)

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


class Player:
    Combination = namedtuple('Combination', ['combotype', 'cards'])

    def __init__(self, name):
        self.name = name
        self.hand = []

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

    def discard(self, combotype, cards):
        cards.sort(key=card_func_key)
        for card in cards:
            self.hand.pop(self.hand.index(card))
        return self.Combination(combotype, cards)

    def sort_hand(self):
        self.hand.sort(key=card_func_key)


# Sorting key for cards:
#   Values are converted to numerical equivalent
#   Suits are also replace by their int representation(rank)
#   Sort cards by their value then suit.
def card_func_key(card):
    return (int(card.value if card.value.isdigit() else HONOURS.get(card.value)),
            -int(SUITS[card.suit].rank))


# Check if cards' combination is valid
def verify_combination(cards):
    if len(cards) == 1:
        return True, 'Single'
    elif len(cards) == 2 and is_pair(cards):
        return True, 'Pair'
    elif len(cards) == 3 and is_three_of_a_kind(cards):
        return True, 'Three of a kind'
    elif len(cards) == 5 :
        if is_straight_flush(cards):
            return True, 'Straight flush'
        elif is_straight(cards):
            return True, 'Straight'
        elif is_flush(cards):
            return True, 'Flush'
        elif is_full_house(cards):
            return True, 'Full house'
        elif is_four_of_a_kind(cards):
            return True, 'Four of a kind'
        else:
            return False, None
    else:
        return False, None


def is_pair(cards):
    return cards[0].value == cards[1].value


def is_three_of_a_kind(cards):
    return cards[0].value == cards[1].value == cards[2].value


def is_straight(cards):
    cards.sort(key=card_func_key)
    card_values = list(map(lambda c: c.value, cards))
    # If cards contains both King and Ace place the Ace at the end of card_values
    if 'King' in card_values and 'Ace' in card_values:
        card_values = card_values[1:] + card_values[:1]
    possible_straight = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    for i in range( len(possible_straight)-4 ):
        if card_values == possible_straight[i:i+5]:
            return True
    return False


def is_flush(cards):
    return all(card.suit==cards[0].suit for card in cards)


def is_full_house(cards):
    card_groups = {}
    for card in cards:
        card_groups.setdefault(card.value, []).append(card)
    return [2, 3] == sorted(map(len, card_groups.values()))


def is_four_of_a_kind(cards):
    card_groups = {}
    for card in cards:
        card_groups.setdefault(card.value, []).append(card)
    return [1, 4] == sorted(map(len, card_groups.values()))


def is_straight_flush(cards):
    return is_straight(cards) and is_flush(cards)


def is_highest(current, former):
    if current.combotype == former.combotype:
        if former.combotype == 'Flush':
            pass
        return current.cards[-1] > former.cards[-1]
    else:
        print('Invalid type of combination played.')
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
    # discard_pile.append(june.discard(combotype, sample_cards))

    card3 = Card('Diamonds', '2')
    card4 = Card('Clubs', '2')
    sample_cards2 = [
        card4
    ]

    pair1 = Player.Combination('Pair', sample_cards1)
    pair2 = Player.Combination('Single', sample_cards2)
    # print(pair1 == pair2)
    # print(sample_cards1 == sample_cards2)
    print(is_highest(pair1, pair2))

    # june.show_hand()

    # Sample play
    # card2 = Card('Hearts', '2')
    # my_discard = [card2]
    # valid, combotype = verify_combination(my_discard)
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

    #                 if suit not in SUITS or \
    #                         value not in (list(map(str, range(1, 11))) + list(HONOURS.values())):
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

    #         valid, combotype = verify_combination(picked_cards)
    #         if valid:
    #             if discard_pile:
    #                 if discard_pile[-1].combotype == 'Single':
    #                     print('Singles combination battle.')
    #                     if picked_cards[0] > discard_pile[-1].cards[0]:
    #                         pass
    #                 # elif discard_pile[-1][0] == 'Pair':
    #                 #     print('Pairs combination battle.')
    #                 # elif discard_pile[-1][0] == 'Three of a kind':
    #                 #     print('Three of a kind combination battle.')
    #                 # else:
    #                 #     print('Five-card hand combination battle.')
    #             discard_pile.append(player.discard(combotype, picked_cards))
    #             pprint(discard_pile)
    #             # player.show_hand()
    #         else:
    #             print('No valid combination found. Try again.')

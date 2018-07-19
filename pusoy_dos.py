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

Suit = namedtuple('Suit', ['name', 'rank', 'uni'])
diamonds = Suit('Diamonds', 1, b'\xE2\x99\xA6'.decode())
hearts = Suit('Hearts', 2, b'\xE2\x99\xA5'.decode())
spades = Suit('Spades', 3, b'\xE2\x99\xA0'.decode())
clubs = Suit('Clubs', 4, b'\xE2\x99\xA3'.decode())

SUITS = {'Diamonds': diamonds,
         'Hearts': hearts,
         'Spades': spades,
         'Clubs': clubs}
ROYALS = {'11': 'Jack', '12': 'Queen', '13': 'King', '1': 'Ace'}

discard_pile = []


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'Card({self.suit}, {self.value})'

    def __str__(self):
        return f'{self.value} of {self.suit}'

    # Part which is quite confusing as without this method the class Player's discard method
    # won't return the result as expected.
    def __eq__(self, other):
        # print(f'{str(self):<17} -------------------------- {other}')
        return self.suit == other.suit and self.value == other.value

    # Reverse comparison of greater than and less than so comparison of card suits match
    # the order of suit ranking where 1 would be the highest.
    # Card values ranking(highest to lowest): 2-A-K-Q-J-10-9...3
    def __gt__(self, other):
        print(f'{self} is greater than {other} in terms of suit.')
        card_value_ranks = map(str, list(range(3, 14)) + [1, 2])
        card_ranks = [(ROYALS.get(value) or value) for value in card_value_ranks]
        print(card_ranks)
        if self.value == other.value:
            return SUITS[self.suit].rank < SUITS[other.suit].rank  ## Test

        return card_ranks.index(self.value) > card_ranks.index(other.value)

    def show(self):
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
            for value in range(1, 14):
                self._cards.append(Card(suit, ROYALS.get(str(value)) or str(value)))

    def shuffle(self):
        # Using Fisher-Yates modern shuffle algorithm
        for i in range(len(self._cards)-1, 0, -1):
            r = math.floor(random() * (i+1))
            self._cards[i], self._cards[r] = self._cards[r], self._cards[i]
        # Or random.shuffle()

    def _show_cards(self):
        for card in self._cards:
            card.show()

    def draw_card(self):
        return self._cards.pop()

    def not_empty(self):
        if self._cards:
            return True


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.Combination = namedtuple('Combination', ['combotype', 'cards'])

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'Player({self.name}, cards_at_hand: {len(self.hand)})'

    def draw(self, deck):
        if deck.not_empty():
            self.hand.append(deck.draw_card())

    def show_hand(self):
        for i, card in enumerate(self.hand):
            print(f'{i+1:<2}', end=' ')
            card.show()

    def discard(self, combotype, cards):
        for card in cards:
            self.hand.pop(self.hand.index(card))
        return self.Combination(combotype, cards)

    def sort_hand(self):
        self.hand.sort(key=card_func_key)


# Sorting key for cards:
# Sort cards by their value then cast them to int. If card is a royal ('Jack', 'Queen', 'King')
# convert them to their corresponding numbers ('11', '12', '13') respectively.
def card_func_key(card):
    royals_reversed = reverse_key_value(ROYALS)
    # return int(royals_reversed.get(card.value)) if not card.value.isdigit() else int(card.value)
    return int(card.value if card.value.isdigit() else royals_reversed.get(card.value))


# Change the dictionary's key to value and value to key.
def reverse_key_value(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        new_dict[value] = key
    return new_dict


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
    card_values = sorted(map(card_func_key, cards))  # Cast card values to int then sort

    # If cards contain a King and an Ace place the Ace at the end of card_values
    if 13 in card_values and 1 in card_values:
        card_values = card_values[1:] + card_values[:1]

    # Casting elements to str then join then check if card_values in sequence
    # of numbers for possible straight combination.
    card_values = ''.join(map(str, card_values))
    sequence = ''.join(map(str, list(range(1, 14)) + [1]))
    return card_values in sequence


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

    players = [john, jane, jess, june]

    # Distribute card to each player
    while deck.not_empty():
        for player in players:
            player.draw(deck)

    # for player in players:
    #     print(f"{player}")
    #     player.show_hand()
    #     print()

    # june.sort_hand()

    # Sample cards to test ranking of card combinations
    # card1 = Card('Hearts', '2')
    # sample_cards = [
    #     card1
    # ]
    # valid, combotype = verify_combination(sample_cards)
    # discard_pile.append(june.discard(combotype, sample_cards))

    # june.show_hand()

    # Sample play
    # card2 = Card('Hearts', '2')
    # my_discard = [card2]
    # valid, combotype = verify_combination(my_discard)
    # print(card2 > card1)

    while True:
        for player in players:
            print(f"{player.name}'s turn.")
            player.sort_hand()
            player.show_hand()

            picked_cards = []
            while True and len(picked_cards) < 5:

                # try:
                    picked_card = input('Choose card to form a combination:(<suit> <value>): ').title()
                    if not picked_card:
                        continue

                    # Optional exit status for faster bug fixing.
                    if picked_card == 'Quit' or picked_card == 'Q':
                        sys.exit()
                    elif picked_card == 'Done' or picked_card == 'D':
                        break

                    suit, value = picked_card.split()

                    if suit not in SUITS or \
                            value not in (list(map(str, range(1, 11))) + list(ROYALS.values())):
                        print(f"Wrong input.")
                        continue

                    card = Card(suit, value)
                    if card not in player.hand:
                        print(f"You don't have the card, {card}")
                    elif card in picked_cards:
                        print(f'{card} is already picked. Choose another one.')
                    else:
                        picked_cards.append(card)
                # except:
                #     print('Invalid input format.')

            valid, combotype = verify_combination(picked_cards)
            if valid:
                if discard_pile:
                    if discard_pile[-1].combotype == 'Single':
                        print('Singles combination battle.')
                        if picked_cards[0] > discard_pile[-1].cards[0]:
                            pass
                    # elif discard_pile[-1][0] == 'Pair':
                    #     print('Pairs combination battle.')
                    # elif discard_pile[-1][0] == 'Three of a kind':
                    #     print('Three of a kind combination battle.')
                    # else:
                    #     print('Five-card hand combination battle.')
                discard_pile.append(player.discard(combotype, picked_cards))
                pprint(discard_pile)
                # player.show_hand()
            else:
                print('No valid combination found. Try again.')



# Todo:
# 1. Create a custom list that list all players.
# 2. List is capable of searching for specific player.
# 3. From that player, we'll provide a next() feature so it will look
# like it is passing a turn.
# 4. Players in list are connected in adjacent order
# 5. If last player reached, iteration goes back at the beginning of list(called cycle)
# 6. Iteration continuous until someone is declared a winner. (a bit wrong)

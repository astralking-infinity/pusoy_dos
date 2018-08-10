from functools import partial

from card import CardPlay, card_func_key, CARD_RANKS, SUIT


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
        return False, 'Straight'
    cards = sorted(cards, key=partial(card_func_key, valueby='rank'))
    card_values = tuple(map(lambda c: c.value, cards))
    for i in range( len(CARD_RANKS)-4 ):
        if card_values == CARD_RANKS[i:i+5]:
            return True, 'Straight'
    return False, 'Straight'


def is_flush(cards):
    return len(cards) == 5 and all(card.suit == cards[0].suit for card in cards), 'Flush'


def is_full_house(cards):
    if len(cards) < 5:
        return False, 'Full house'
    card_groups = {}
    for card in cards:
        card_groups.setdefault(card.value, []).append(card)
    return [2, 3] == sorted(map(len, card_groups.values())), 'Full house'


def is_four_of_a_kind(cards):
    if len(cards) < 5:
        return False, 'Four of a kind'
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
            # Comparing two five-card combination with same type
            if self.combotype == other.combotype:
                if self.combotype in ('Full house', 'Four of a kind', 'Straight'):
                    return self.cards[-1] > other.cards[-1]
                else:  # self.combotype in ('Flush', 'Straight flush')
                    if self.cards[-1].suit == other.cards[-1].suit:
                        return self.cards[-1].value > other.cards[-1].value
                    return SUIT[self.cards[-1].suit].rank < SUIT[other.cards[-1].suit].rank
            else:
                return CardPlay.five_card_group[self.combotype] > CardPlay.five_card_group[other.combotype]
    else:
        # print(f"Invalid match up.")
        return False

from functools import partial

from card import card_func_key


class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next

    def __repr__(self):
        return f'{self.__class__.__name__}({self.data!r})'


class ActivePlayer:
    """A class for managing list of players in a continuous cycle
    or until winner has been decided."""

    def __init__(self, *players):
        self._first = None
        self._last = None
        self._turn = None
        self._size = 0
        self.set(*players)

    def __repr__(self):
        current = self._first
        player_objs = []
        for i in range(self._size):
            player_objs.append(current.get_data())
            current = current.get_next()
        return f"{self.__class__.__name__}({', '.join(map(str, player_objs))})"

    def __str__(self):
        current = self._first
        _players = []
        for i in range(self._size):
            _players.append(f'Player {i+1}: {current.get_data().name}')
            current = current.get_next()
        return '\n'.join(_players)

    def __iter__(self):
        self._turn = None
        return self

    def __next__(self):
        if self._turn:
            self._turn = self._turn.get_next()
            if not self._turn:
                raise StopIteration
        else:
            self._turn = self._first
        return self._turn.get_data()

    def set(self, *players):
        if players:
            for player in players:
                node = Node(player)
                if self._last:
                    self._last.set_next(node)
                else:
                    self._first = node
                self._last = node
                self._size += 1
            # self._last.set_next(self._first)

    def add(self, player):
        node = Node(player)
        self._last.set_next(node)
        node.set_next(self._first)
        self._last = node
        self._size += 1

    def next_turn(self):
        if self._turn:
            turn = self._turn.get_next()
            self._turn = turn if turn else self._first
        else:
            self._turn = self._first
        return self._turn.get_data()

    def assign_control(self, player):
        self._turn = self.search(player)
        return self._turn.get_data()

    def search(self, player):
        # Test the correctness of method
        current = self._first
        found = False
        while not found:
            if current.get_data() == player:
                found = True
            else:
                current = current.get_next()
        return current

    def remove(self, player):
        # Somehow needs to return a value indicating that a value has been
        # removed
        current = self._first
        previous = None
        found = False
        while not found:
            if current.get_data() == player:
                self._size -= 1
                found = True
            else:
                previous = current
                current = current.get_next()
        if not previous:
            self._first = current.get_next()
            self._last.set_next(self._first)
        else:
            if self._last == current:
                self._last = previous
            previous.set_next(current.get_next())
        return found

    def get_size(self):
        return self._size

    def get_first(self):
        return self._first

    def get_last(self):
        return self._last


class Player:
    count = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        Player.count += 1

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r})'

    def draw(self, deck):
        if deck.not_empty():
            self.hand.append(deck.draw_card())

    def show_hand(self):
        cards = []
        for i, card in enumerate(self.hand):
            cards.append(card.show(display=False))
        print('-'.join(cards))

    def play(self, card_play):
        # cards = sorted(cards, key=partial(card_func_key, valueby='rank'))
        for card in card_play.cards:
            self.hand.pop(self.hand.index(card))
        return card_play

    def discard(self, card):
        if card in self.hand:
            self.hand.pop(self.hand.index(card))

    def sort_hand(self):
        self.hand.sort(key=partial(card_func_key, valueby='rank'))

    def card_count(self):
        return len(self.hand)

    def has_empty_hand(self):
        return not self.hand


if __name__ == '__main__':
    from card import Deck

    """Reference: Implementing an Unordered List: Linked Lists
    http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementinganUnorderedListLinkedLists.html
    """

    deck = Deck()
    deck.shuffle()

    john = Player('John')
    jane = Player('Jane')
    jess = Player('Jess')
    june = Player('June')
    jack = Player('Jack')

    player_list = ActivePlayer(john, jane, jess, june)
    # player_list.in_control(june)
    # player_list.remove(june)
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # player_list.show_first()
    # print(player_list.get_size())
    player_list.add(jack)
    # player_list.show_players()
    print(player_list)
    print(player_list.get_size())

""" player_nodes.py

Data structure for listing players.
"""


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
    """ A class for managing list of players in a continuous cycle
        or until winner has been decided.
    """

    def __init__(self, *players):
        self.first = None
        self.last = None
        self.turn = None
        self.size = 0
        self.set(*players)

    def __repr__(self):
        current = self.first
        player_objs = []
        for i in range(self.size()):
            player_objs.append(current.get_data())
            current = current.get_next()
        return f"{self.__class__.__name__}({', '.join(map(str, player_objs))})"

    def __str__(self):
        current = self.first
        _players = []
        for i in range(self.size):
            _players.append(f'Player {i+1}: {current.get_data().name}')
            current = current.get_next()
        return '\n'.join(_players)

    # def __iter__(self):
    #     return iter(self.next_turn())

    def set(self, *players):
        if players:
            for player in players:
                node = Node(player)
                if self.last:
                    self.last.set_next(node)
                else:
                    self.first = node
                self.last = node
                self.size += 1
            self.last.set_next(self.first)

    def add(self, player):
        node = Node(player)
        self.last.set_next(node)
        node.set_next(self.first)
        self.last = node
        self.size += 1

    def next_turn(self):
        if self.turn:
            self.turn = self.turn.get_next()
        else:
            self.turn = self.first
        return self.turn.get_data()

    def upper_hand(self, player):
        self.turn = self.search(player)
        print(f'Advantage: {self.turn.get_data().name}')
        return self.turn.get_data()

    def search(self, player):
        # Test the correctness of method
        current = self.first
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
        current = self.first
        previous = None
        found = False
        while not found:
            if current.get_data() == player:
                found = True
            else:
                previous = current
                current = current.get_next()
        if not previous:
            self.first = current.get_next()
            self.last.set_next(self.first)
        else:
            if self.last == current:
                self.last = previous
            previous.set_next(current.get_next())

    def get_size(self):
        return self.size

    def _show_first(self):
        print(self.first)

    def _show_last(self):
        print(self.last)


if __name__ == '__main__':
    from pusoy_dos import Player, Deck

    """ Reference: Implementing an Unordered List: Linked Lists
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
    # player_list.upper_hand(june)
    # player_list.remove(june)
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # print(player_list.next_turn())
    # player_list.show_first()
    # print(player_list.size())
    player_list.add(jack)
    # player_list.show_players()
    print(player_list)
    print(player_list.get_size())

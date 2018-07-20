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
        return f'Node(data={self.data}, next=Node({self.next.data}))'


class ActivePlayer:
    """ A class for managing list of players in a continuous cycle
        or until winner has been decided.
    """

    def __init__(self, *players):
        self.head = None
        self.tail = None
        self.turn = None
        self.set(*players)

    def set(self, *players):
        for player in players:
            node = Node(player)
            if self.tail:
                self.tail.set_next(node)
            else:
                self.head = node
            self.tail = node
        self.tail.set_next(self.head)

    def add(self, player):
        node = Node(player)
        self.tail.set_next(node)
        node.set_next(self.head)
        self.tail = node

    def next_turn(self):
        if self.turn:
            self.turn = self.turn.get_next()
        else:
            self.turn = self.head
        return self.turn.get_data()

    def upper_hand(self, player):
        self.turn = self.search(player)
        print(f'Advantage: {self.turn.get_data().name}')
        return self.turn.get_data()

    def search(self, player):
        current = self.head
        found = False
        while not found:
            if current.get_data() == player:
                found = True
            else:
                current = current.get_next()
        return current

    def remove(self, player):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.get_data() == player:
                found = True
            else:
                previous = current
                current = current.get_next()
        if not previous:
            self.head = current.get_next()
            self.tail.set_next(self.head)
        else:
            if self.tail == current:
                self.tail = previous
            previous.set_next(current.get_next())

    def size(self):
        current = self.head
        count = 1 if current else 0
        while current and current != self.tail:
            current = current.get_next()
            count += 1
        return count

    def _show_head(self):
        print(self.head)

    def _show_tail(self):
        print(self.tail)

    def show_players(self):
        current = self.head
        for i in range(self.size()):
            print(f'Player {i+1}: {current.get_data().name}')
            current = current.get_next()


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
    # player_list.show_head()
    # print(player_list.size())
    player_list.add(jack)
    player_list.show_players()

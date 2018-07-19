""" player_nodes.py

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
        return f'Node(data={self.data}, next={self.next.data})'


class ActivePlayer:

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
                self.tail = node
            else:
                self.head = node
                self.tail = node
        self.tail.set_next(self.head)

    def next_turn(self):
        if self.turn:
            self.turn = self.turn.get_next()
        else:
            self.turn = self.head
        return self.turn.get_data()

    def upper_hand(self, player):
        self.turn = self.search(player)
        print(f'Advantage: {self.turn.get_data()}')

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

    def show_head(self):
        print(self.head)

    def show_tail(self):
        print(self.tail)


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

    player_list = ActivePlayer(john,jane,jess,june)
    player_list.upper_hand(june)
    player_list.remove(june)
    print(player_list.next_turn())
    print(player_list.next_turn())
    print(player_list.next_turn())
    print(player_list.next_turn())
    print(player_list.next_turn())
    print(player_list.next_turn())
    player_list.show_head()


    # Extra todo:
    # Difference between __str__ and __repr__

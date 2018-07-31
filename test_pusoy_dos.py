import unittest

from pusoy_dos import *


class TestPusoyDos(unittest.TestCase):

    def test_is_single(self):
        single = [Card('Clubs', '3')]
        self.assertEqual(is_single(single), (True, 'Single'))

    def test_is_pair(self):
        pair1 = [Card('Hearts', 'Queen'), Card('Clubs', 'Queen')]
        pair2 = [Card('Diamonds', 'Ace'), Card('Spades', '3')]
        self.assertEqual(is_pair(pair1), (True, 'Pair'))
        self.assertEqual(is_pair(pair2), (False, 'Pair'))

    def test_is_three_of_a_kind(self):
        trio1 = [Card('Hearts', 'Queen'),
                 Card('Clubs', 'Queen'),
                 Card('Diamonds', 'Queen')]
        trio2 = [Card('Spades', '7'),
                 Card('Clubs', '10'),
                 Card('Diamonds', '7')]
        self.assertEqual(is_three_of_a_kind(trio1), (True, 'Three of a kind'))
        self.assertEqual(is_three_of_a_kind(trio2), (False, 'Three of a kind'))

    def test_is_flush(self):
        five_hand1 = [Card('Clubs', 'Queen'),
                      Card('Clubs', '7'),
                      Card('Clubs', '8'),
                      Card('Clubs', '3'),
                      Card('Clubs', 'Jack')]
        five_hand2 = [Card('Hearts', '5'),
                      Card('Spades', 'King'),
                      Card('Diamonds', '2'),
                      Card('Spades', '6'),
                      Card('Spades', '7')]
        self.assertEqual(is_flush(five_hand1), (True, 'Flush'))
        self.assertEqual(is_flush(five_hand2), (False, 'Flush'))

    def test_is_four_of_a_kind(self):
        five_hand1 = [Card('Hearts', 'Queen'),
                      Card('Spades', '4'),
                      Card('Diamonds', '4'),
                      Card('Hearts', '4'),
                      Card('Clubs', '4')]
        five_hand2 = [Card('Clubs', 'Queen'),
                      Card('Diamonds', 'Jack'),
                      Card('Hearts', '3'),
                      Card('Clubs', 'Jack'),
                      Card('Spades', 'Jack')]
        self.assertEqual(is_four_of_a_kind(five_hand1), (True, 'Four of a kind'))
        self.assertEqual(is_four_of_a_kind(five_hand2), (False, 'Four of a kind'))

    def test_is_full_house(self):
        five_hand1 = [Card('Hearts', 'Queen'),
                      Card('Spades', '4'),
                      Card('Diamonds', '4'),
                      Card('Hearts', 'Queen'),
                      Card('Clubs', '4')]
        five_hand2 = [Card('Clubs', 'Queen'),
                      Card('Diamonds', 'Jack'),
                      Card('Hearts', '3'),
                      Card('Clubs', 'Jack'),
                      Card('Spades', 'Jack')]
        self.assertEqual(is_full_house(five_hand1), (True, 'Full house'))
        self.assertEqual(is_full_house(five_hand2), (False, 'Full house'))

    def test_is_straight(self):
        five_hand1 = [Card('Hearts', 'Queen'),
                      Card('Spades', 'Jack'),
                      Card('Diamonds', '10'),
                      Card('Hearts', 'King'),
                      Card('Clubs', 'Ace')]
        five_hand2 = [Card('Clubs', '3'),
                      Card('Diamonds', '4'),
                      Card('Hearts', '3'),
                      Card('Clubs', '5'),
                      Card('Spades', '6')]
        self.assertEqual(is_straight(five_hand1), (True, 'Straight'))
        self.assertEqual(is_straight(five_hand2), (False, 'Straight'))

    def test_is_straight_flush(self):
        five_hand1 = [Card('Clubs', 'Queen'),
                      Card('Clubs', 'Jack'),
                      Card('Clubs', '10'),
                      Card('Clubs', 'King'),
                      Card('Clubs', 'Ace')]
        five_hand2 = [Card('Clubs', '3'),
                      Card('Clubs', '4'),
                      Card('Clubs', '3'),
                      Card('Clubs', '5'),
                      Card('Clubs', '6')]
        self.assertEqual(is_straight_flush(five_hand1), (True, 'Straight flush'))
        self.assertEqual(is_straight_flush(five_hand2), (False, 'Straight flush'))

    def test_is_higher(self):
        single1 = Player.Combination('Single', [Card('Clubs', '2')])
        single2 = Player.Combination('Single', [Card('Diamonds', '3')])
        single3 = Player.Combination('Single', [Card('Diamonds', '5')])
        single4 = Player.Combination('Single', [Card('Clubs', '5')])
        self.assertTrue(is_higher(single1, single2))
        self.assertTrue(is_higher(single3, single4))

        pair1 = Player.Combination('Pair', [Card('Clubs', '2'), Card('Spades', '2')])
        pair2 = Player.Combination('Pair', [Card('Hearts', '3'), Card('Diamonds', '3')])
        pair3 = Player.Combination('Pair', [Card('Clubs', 'King'), Card('Spades', 'King')])
        pair4 = Player.Combination('Pair', [Card('Hearts', 'King'), Card('Diamonds', 'King')])
        self.assertTrue(is_higher(pair1, pair2))
        self.assertFalse(is_higher(pair3, pair4))


if __name__ == '__main__':
    unittest.main()

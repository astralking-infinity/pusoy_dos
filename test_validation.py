import unittest

from card import Card, CardPlay
from validation import *


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
        triple1 = [Card('Hearts', 'Queen'),
                   Card('Clubs', 'Queen'),
                   Card('Diamonds', 'Queen')]
        triple2 = [Card('Spades', '7'),
                   Card('Clubs', '10'),
                   Card('Diamonds', '7')]
        self.assertEqual(is_three_of_a_kind(triple1), (True, 'Three of a kind'))
        self.assertEqual(is_three_of_a_kind(triple2), (False, 'Three of a kind'))

    def test_is_flush(self):
        cards1 = [Card('Clubs', 'Queen'),
                  Card('Clubs', '7'),
                  Card('Clubs', '8'),
                  Card('Clubs', '3'),
                  Card('Clubs', 'Jack')]
        cards2 = [Card('Hearts', '5'),
                  Card('Spades', 'King'),
                  Card('Diamonds', '2'),
                  Card('Spades', '6'),
                  Card('Spades', '7')]
        self.assertEqual(is_flush(cards1), (True, 'Flush'))
        self.assertEqual(is_flush(cards2), (False, 'Flush'))

    def test_is_four_of_a_kind(self):
        cards1 = [Card('Hearts', 'Queen'),
                  Card('Spades', '4'),
                  Card('Diamonds', '4'),
                  Card('Hearts', '4'),
                  Card('Clubs', '4')]
        cards2 = [Card('Clubs', 'Queen'),
                  Card('Diamonds', 'Jack'),
                  Card('Hearts', '3'),
                  Card('Clubs', 'Jack'),
                  Card('Spades', 'Jack')]
        self.assertEqual(is_four_of_a_kind(cards1), (True, 'Four of a kind'))
        self.assertEqual(is_four_of_a_kind(cards2), (False, 'Four of a kind'))

    def test_is_full_house(self):
        cards1 = [Card('Hearts', 'Queen'),
                  Card('Spades', '4'),
                  Card('Diamonds', '4'),
                  Card('Hearts', 'Queen'),
                  Card('Clubs', '4')]
        cards2 = [Card('Clubs', 'Queen'),
                  Card('Diamonds', 'Jack'),
                  Card('Hearts', '3'),
                  Card('Clubs', 'Jack'),
                  Card('Spades', 'Jack')]
        self.assertEqual(is_full_house(cards1), (True, 'Full house'))
        self.assertEqual(is_full_house(cards2), (False, 'Full house'))

    def test_is_straight(self):
        cards1 = [Card('Hearts', 'Queen'),
                  Card('Spades', 'Jack'),
                  Card('Diamonds', '10'),
                  Card('Hearts', 'King'),
                  Card('Clubs', 'Ace')]
        cards2 = [Card('Clubs', '3'),
                  Card('Diamonds', '4'),
                  Card('Hearts', '3'),
                  Card('Clubs', '5'),
                  Card('Spades', '6')]
        self.assertEqual(is_straight(cards1), (True, 'Straight'))
        self.assertEqual(is_straight(cards2), (False, 'Straight'))

    def test_is_straight_flush(self):
        cards1 = [Card('Clubs', 'Queen'),
                  Card('Clubs', 'Jack'),
                  Card('Clubs', '10'),
                  Card('Clubs', 'King'),
                  Card('Clubs', 'Ace')]
        cards2 = [Card('Clubs', '3'),
                  Card('Clubs', '4'),
                  Card('Clubs', '3'),
                  Card('Clubs', '5'),
                  Card('Clubs', '6')]
        self.assertEqual(is_straight_flush(cards1), (True, 'Straight flush'))
        self.assertEqual(is_straight_flush(cards2), (False, 'Straight flush'))

    def test_is_higher(self):
        # Test single type
        single1 = CardPlay('Single', [Card('Clubs', '2')])
        single2 = CardPlay('Single', [Card('Hearts', '3')])
        single3 = CardPlay('Single', [Card('Diamonds', '3')])
        self.assertTrue(is_higher(single1, single2))
        self.assertFalse(is_higher(single2, single3))

        # Test pair type
        pair1 = CardPlay('Pair', [Card('Clubs', '2'), Card('Spades', '2')])
        pair2 = CardPlay('Pair', [Card('Clubs', 'King'), Card('Spades', 'King')])
        pair3 = CardPlay('Pair', [Card('Hearts', 'King'), Card('Diamonds', 'King')])
        self.assertTrue(is_higher(pair1, pair2))
        self.assertFalse(is_higher(pair2, pair3))

        # Test three of a kind type
        triple1 = CardPlay('Three of a kind', [Card('Clubs', 'Queen'), Card('Hearts', 'Queen'), Card('Diamonds', 'Queen')])
        triple2 = CardPlay('Three of a kind', [Card('Spades', '10'), Card('Hearts', '10'), Card('Diamonds', '10')])
        triple3 = CardPlay('Three of a kind', [Card('Clubs', 'King'), Card('Spades', 'King'), Card('Hearts', 'King')])
        self.assertTrue(is_higher(triple1, triple2))
        self.assertFalse(is_higher(triple2, triple3))

        # Test straight flush type
        straight_flush1 = CardPlay('Straight Flush', [Card('Diamonds', '10'),
                                                      Card('Diamonds', 'Jack'),
                                                      Card('Diamonds', 'Queen'),
                                                      Card('Diamonds', 'King'),
                                                      Card('Diamonds', 'Ace')])
        straight_flush2 = CardPlay('Straight Flush', [Card('Spades', '6'),
                                                      Card('Spades', '7'),
                                                      Card('Spades', '8'),
                                                      Card('Spades', '9'),
                                                      Card('Spades', '10')])
        straight_flush3 = CardPlay('Straight Flush', [Card('Hearts', '6'),
                                                      Card('Hearts', '7'),
                                                      Card('Hearts', '8'),
                                                      Card('Hearts', '9'),
                                                      Card('Hearts', '10')])
        self.assertTrue(is_higher(straight_flush1, straight_flush2))
        self.assertFalse(is_higher(straight_flush2, straight_flush3))

        # Test straight type
        straight1 = CardPlay('Straight', [Card('Diamonds', '10'),
                                          Card('Hearts', 'Jack'),
                                          Card('Diamonds', 'Queen'),
                                          Card('Spades', 'King'),
                                          Card('Hearts', 'Ace')])
        straight2 = CardPlay('Straight', [Card('Spades', '10'),
                                          Card('Hearts', 'Jack'),
                                          Card('Hearts', 'Queen'),
                                          Card('Diamonds', 'King'),
                                          Card('Spades', 'Ace')])
        straight3 = CardPlay('Straight', [Card('Spades', 'Jack'),
                                          Card('Hearts', 'Queen'),
                                          Card('Diamonds', 'King'),
                                          Card('Diamonds', 'Ace'),
                                          Card('Hearts', '2')])
        self.assertTrue(is_higher(straight1, straight2))
        self.assertFalse(is_higher(straight2, straight3))

        # Test flush type
        flush1 = CardPlay('Flush', [Card('Diamonds', '3'),
                                    Card('Diamonds', '6'),
                                    Card('Diamonds', '7'),
                                    Card('Diamonds', '9'),
                                    Card('Diamonds', 'Ace')])
        flush2 = CardPlay('Flush', [Card('Spades', '5'),
                                    Card('Spades', '6'),
                                    Card('Spades', '7'),
                                    Card('Spades', '8'),
                                    Card('Spades', 'Jack')])
        flush3 = CardPlay('Flush', [Card('Hearts', '4'),
                                    Card('Hearts', '5'),
                                    Card('Hearts', '7'),
                                    Card('Hearts', '8'),
                                    Card('Hearts', 'King')])
        self.assertTrue(is_higher(flush1, flush2))
        self.assertFalse(is_higher(flush2, flush3))

        # Test full house type
        full_house1 = CardPlay('Full house', [Card('Spades', '9'),
                                              Card('Diamonds', '9'),
                                              Card('Clubs', '2'),
                                              Card('Spades', '2'),
                                              Card('Hearts', '2')])
        full_house2 = CardPlay('Full house', [Card('Clubs', '8'),
                                              Card('Clubs', '5'),
                                              Card('Spades', '5'),
                                              Card('Hearts', '5'),
                                              Card('Diamonds', '5')])
        full_house3 = CardPlay('Full house', [Card('Hearts', '8'),
                                              Card('Clubs', 'Queen'),
                                              Card('Spades', 'Queen'),
                                              Card('Hearts', 'Queen'),
                                              Card('Diamonds', 'Queen')])
        self.assertTrue(is_higher(full_house1, full_house2))
        self.assertFalse(is_higher(full_house2, full_house3))

        # Test four of a kind type
        quad1 = CardPlay('Four of a kind', [Card('Diamonds', '6'),
                                            Card('Clubs', '2'),
                                            Card('Spades', '2'),
                                            Card('Hearts', '2'),
                                            Card('Diamonds', '2')])
        quad2 = CardPlay('Four of a kind', [Card('Clubs', '8'),
                                            Card('Clubs', '5'),
                                            Card('Spades', '5'),
                                            Card('Hearts', '5'),
                                            Card('Diamonds', '5')])
        quad3 = CardPlay('Four of a kind', [Card('Hearts', '8'),
                                            Card('Clubs', 'Queen'),
                                            Card('Spades', 'Queen'),
                                            Card('Hearts', 'Queen'),
                                            Card('Diamonds', 'Queen')])
        self.assertTrue(is_higher(quad1, quad2))
        self.assertFalse(is_higher(quad2, quad3))

        # Test five-card category comparison
        self.assertTrue(is_higher(full_house1, flush1))
        self.assertTrue(is_higher(quad1, full_house1))

        # Test comparison of 2 cards played with different categories.
        self.assertFalse(is_higher(single1, pair1))
        self.assertFalse(is_higher(triple1, quad1))


if __name__ == '__main__':
    unittest.main()

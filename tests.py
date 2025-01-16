from collections import Counter
import unittest

from poker_reinforcement_learning.deck import *

class TestRankHand(unittest.TestCase):
    def test_royal_flush_1(self):
        hand = [Card('10', 'red', 'Heart'), Card('Jack', 'red', 'Heart'),
                Card('Queen', 'red', 'Heart'), Card('King', 'red', 'Heart'),
                Card('Ace', 'red', 'Heart')]
        result = rank_hand(hand)
        self.assertEqual(result, (10, [14]), "Should be a Royal Flush")

    def test_royal_flush_7(self):
        hand = [Card('10', 'red', 'Heart'), Card('Jack', 'red', 'Heart'),
                Card('Queen', 'red', 'Heart'), Card('King', 'red', 'Heart'),
                Card('Ace', 'red', 'Heart'), Card('Ace', 'black', 'Spade') ,Card('3', 'red', 'Diamond')]
        result = rank_hand(hand)
        self.assertEqual(result, (10, [14]), "Should be a Royal Flush")
    
    def test_royal_flush_2(self):
        hand = [Card('10', 'red', 'Diamond'), Card('Jack', 'red', 'Diamond'),
                Card('Queen', 'red', 'Diamond'), Card('King', 'red', 'Diamond'),
                Card('Ace', 'red', 'Diamond')]
        result = rank_hand(hand)
        self.assertEqual(result, (10, [14]), "Should be a Royal Flush")

    def test_straight_flush(self):
        hand = [Card('9', 'black', 'Diamond'), Card('10', 'black', 'Diamond'),
                Card('Jack', 'black', 'Diamond'), Card('Queen', 'black', 'Diamond'),
                Card('King', 'black', 'Diamond')]
        result = rank_hand(hand)
        self.assertEqual(result, (9, [13]), "Should be a Straight Flush")

    def test_straight_flush_low(self):
        hand = [Card('4', 'black', 'Clover'), Card('2', 'black', 'Clover'),
                Card('Ace', 'black', 'Clover'), Card('5', 'black', 'Clover'),
                Card('3', 'black', 'Clover')]
        result = rank_hand(hand)
        self.assertEqual(result, (9, [14]), "Should be a Straight Flush")


    def test_4_of_kind_1(self):
        hand = [Card('8', 'red', 'Heart'), Card('8', 'black', 'Spade'),
                Card('8', 'red', 'Diamond'), Card('8', 'black', 'Clover'),
                Card('Ace', 'red', 'Heart')]
        result = rank_hand(hand)

        self.assertEqual(result, (8, [8, 14]), "Should be a Four of a Kind")

    def test_4_of_kind_2(self):
        hand = [Card('King', 'red', 'Heart'), Card('King', 'black', 'Spade'),
                Card('King', 'red', 'Diamond'), Card('King', 'black', 'Clover'),
                Card('5', 'red', 'Diamond')]
        result = rank_hand(hand)

        self.assertEqual(result, (8, [13, 5]), "Should be a Four of a Kind")

    def test_full_house_1(self):
        hand = [Card('King', 'red', 'Heart'), Card('King', 'black', 'Spade'),
                Card('King', 'red', 'Diamond'), Card('5', 'black', 'Clover'),
                Card('5', 'red', 'Diamond')]
        result = rank_hand(hand)

        
        self.assertEqual(result, (7, [13, 5]), "Should be a Full")

    def test_full_house_2(self):
        hand = [Card('Ace', 'red', 'Heart'), Card('Ace', 'black', 'Spade'),
                Card('Ace', 'red', 'Diamond'), Card('2', 'black', 'Clover'),
                Card('2', 'red', 'Diamond')]
        result = rank_hand(hand)

        
        self.assertEqual(result, (7, [14, 2]), "Should be a Full")

    def test_flush_1(self):
        hand = [Card('3', 'red', 'Heart'), Card('Ace', 'red', 'Heart'),
                Card('6', 'red', 'Heart'), Card('10', 'red', 'Heart'),
                Card('2', 'red', 'Heart')]
        result = rank_hand(hand)

        
        self.assertEqual(result, (6, [14, 10, 6, 3, 2]), "Should be a Flush")

    def test_flush_2(self):
        hand = [Card('5', 'red', 'Heart'), Card('8', 'red', 'Heart'),
                Card('6', 'red', 'Heart'), Card('4', 'red', 'Heart'),
                Card('2', 'red', 'Heart')]
        result = rank_hand(hand)

        
        self.assertEqual(result, (6, [ 8, 6, 5,4, 2]), "Should be a Flush")

    def test_flush_3(self):
        hand = [Card('8', 'red', 'Heart'), Card('8', 'red', 'Heart'),
                Card('6', 'red', 'Heart'), Card('4', 'red', 'Heart'),
                Card('2', 'red', 'Heart')]
        result = rank_hand(hand)

        
        self.assertEqual(result, (6, [8, 8, 6, 4, 2]), "Should be a Flush")

    def test_straight(self):
        hand = [Card('4', 'red', 'Heart'), Card('6', 'black', 'Clover'),
                Card('5', 'black', 'Spade'), Card('7', 'black', 'Spade'),
                Card('3', 'black', 'Spade')]
        result = rank_hand(hand)
        self.assertEqual(result, (5, [7]), "Should be a Straight")
    def test_straight_low(self):
        hand = [Card('4', 'red', 'Heart'), Card('2', 'black', 'Clover'),
                Card('Ace', 'black', 'Spade'), Card('5', 'black', 'Spade'),
                Card('3', 'black', 'Spade')]
        result = rank_hand(hand)
        self.assertEqual(result, (5, [14]), "Should be a Straight")

    def test_one_pair(self):
        hand = [Card('8', 'red', 'Heart'), Card('8', 'black', 'Diamond'),
                Card('3', 'red', 'Spade'), Card('6', 'black', 'Clover'),
                Card('Ace', 'red', 'Heart')]

        result = rank_hand(hand)

        self.assertEqual(result, (2, [8, 14, 6, 3]), "Should be a One Pair")

    def test_high_card_1(self):
        hand = [Card('8', 'red', 'Heart'), Card('2', 'black', 'Diamond'),
                Card('3', 'red', 'Spade'), Card('6', 'black', 'Clover'),
                Card('Ace', 'red', 'Heart')]

        result = rank_hand(hand)

        self.assertEqual(result, (1, [14, 8, 6, 3, 2]), "Should be a High Card")

    def test_high_card_2(self):
        hand = [Card('9', 'red', 'Heart'), Card('2', 'red', 'Heart'),
                Card('7', 'red', 'Spade'), Card('3', 'black', 'Diamond'),
                Card('King', 'black', 'Clover')]

        result = rank_hand(hand)

        self.assertEqual(result, (1, [13, 9, 7, 3, 2]), "Should be a High Card")


def rank_hand(hand):
    # Helper function to rank the hand
    # Returns a tuple with two values:
    # - The rank of the hand (higher is better)
    # - The value(s) used for tie-breaking if ranks are equal
    def is_subarray(subarray, array):
        # Helper function to check if subarray is a subarray of array
        m, n = len(subarray), len(array)
        i = 0
        while i <= n - m:
            if array[i:i + m] == subarray:
                return True  # subarray found
            i += 1
        return False
        n = len(array)
        print(array)
        if n < 5:
            return False

        return array[:-5] == subarray
    def has_flush(suits):
        # Helper function to check for a flush
        # Returns True if there are 5 or more cards of the same suit, False otherwise
        suit_counts = Counter(suits)
        return any(count >= 5 for count in suit_counts.values())
    def has_consecutive_values(arr):
        n = len(arr)
        if n < 5:
            return False, []
        sorted_arr = sorted(arr)
        for i in range(n - 4):
            sub_array = sorted_arr[i : i + 5]
            # print(sub_array)
            if all((sub_array[j] + 1) % 13 == sub_array[j + 1] % 13 for j in range(4)) or set(sub_array) == {12, 0, 1, 2, 3}:
                
                return True, sub_array
        return False, []
    values = [card.value for card in hand]
    suits = [card.suit for card in hand]

    flush = has_flush(suits)



    

    if is_subarray([10, 11, 12, 13, 14], sorted(values)) and flush:
        # print("Royal Flush!")
        return (10, [14])

    
    straight_values = [value - 2 for value in values]

    

    
    if flush:
        is_straight_flush, returned = has_consecutive_values(straight_values)
        if is_straight_flush:
        # print("Straight Flush!")
            return (9, [[value + 2 for value in returned][4]])

        # If it's not a straight flush but all suits are the same, it's a flush
        # Note: You should sort the values in descending order, not just reverse
        return (6, sorted(values, reverse=True))


    for value, count in Counter(values).items():
        if count == 4:
            # print("Four of a kind!")
            return (8, [value, max(set(values) - {value})])

    three_of_a_kind = None
    pair = None
    for value, count in Counter(values).items():
        if count == 3:
            three_of_a_kind = value
        elif count == 2:
            pair = value

    if three_of_a_kind is not None and pair is not None:
        # print("Full House!")
        return (7, [three_of_a_kind, pair])

    
    is_straight, returned = has_consecutive_values(straight_values)
    if (is_straight):
        # print("Straight!") 
        return (5, [[value + 2 for value in returned][4]])

    for value, count in Counter(values).items():
        if count == 3:
            # print("3 of a kind!")
            return (4, [value] + sorted(set(values) - {value}, reverse=True)[:2])

    pairs = [value for value, count in Counter(values).items() if count == 2]
    if len(pairs) >= 2:
        # print("Two Pair!")
        return (3, sorted(pairs, reverse=True) + sorted(set(values) - set(pairs), reverse=True)[:1])

    for value, count in Counter(values).items():
        if count == 2:
            # print("One Pair!")
            return (2, [value] + sorted(set(values) - {value}, reverse=True)[:3])

    # print("High Card!")
    return (1, sorted(values, reverse=True))

if __name__ == '__main__':
    unittest.main()

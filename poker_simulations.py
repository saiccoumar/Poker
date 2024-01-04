from deck import *
from collections import Counter
import numpy as np
import json

flag = False
def cprint(str):
    if flag:
        print(str)
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

class TexasHoldem:
    winning_hand_frequency = {
            "Royal Flush": 0,
            "Straight Flush": 0,
            "Four of a Kind": 0,
            "Full House": 0,
            "Flush": 0,
            "Straight": 0,
            "Three of a Kind": 0,
            "Two Pair": 0,
            "One Pair": 0,
            "High Card": 0,
        }
    all_hands_frequency = {
        "Royal Flush": 0,
        "Straight Flush": 0,
        "Four of a Kind": 0,
        "Full House": 0,
        "Flush": 0,
        "Straight": 0,
        "Three of a Kind": 0,
        "Two Pair": 0,
        "One Pair": 0,
        "High Card": 0,
    }
    
    def __init__(self, num_players=2):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = num_players
        self.community_cards = []
        self.player_hands = [[] for _ in range(num_players)]
        self.wins_frequency = [[0] * 13 for _ in range(13)]  # 2D array for wins
        self.losses_frequency = [[0] * 13 for _ in range(13)]  # 2D array for losses

    def deal_hole_cards(self):
        for _ in range(2):
            for hand in self.player_hands:
                hand.append(self.deck.deal_card())

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            self.community_cards.append(self.deck.deal_card())

    def determine_winner(self):
        all_hands = [hand + self.community_cards for hand in self.player_hands]

        best_hands = [rank_hand(player_hand) for player_hand in all_hands]

        

        # Sort the best hands by rank and then by the highest card value
        sorted_best_hands = sorted(enumerate(best_hands), key=lambda x: (x[1][0], x[1][1]), reverse=True)

        # Determine the winner
        winner_index = sorted_best_hands[0][0]  # Get the index of the first (highest) hand
        winning_hand = all_hands[winner_index]
        with open("winninghandslog.txt",'a') as f:
            print([str(hand) for hand in winning_hand], file=f) 
        

        # Update winning_hand_frequency dictionary based on the hand rank
        rank, _ = best_hands[winner_index]
        rank_mapping = {
            10: "Royal Flush",
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card",
        }

        for i in all_hands:
            rank, _ = rank_hand(i)
            self.all_hands_frequency[rank_mapping[rank]] += 1

        hand_category = rank_mapping[rank]
        
        cprint("Winning Hand:" + rank_mapping[rank]+" with rank "+ str(rank))
        

        cprint(self.winning_hand_frequency)
        self.winning_hand_frequency[hand_category] += 1
        cprint(self.winning_hand_frequency)
        

        return winner_index + 1

    def record_result(self, result, first_card_value, second_card_value):
        # Values range from 2-14. We need to standardize them to 0-12.
        if result == "win":
            self.wins_frequency[first_card_value-2][second_card_value-2] += 1
        elif result == "loss":
            self.losses_frequency[first_card_value-2][second_card_value-2] += 1

    def reset_deck(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.player_hands = [[] for _ in range(self.num_players)]

    def print_state(self):
        print("\nCommunity Cards:", [str(card) for card in self.community_cards])
        for i, hand in enumerate(self.player_hands):
            print(f"Player {i + 1}'s hand: {[str(card) for card in hand]}")

    def play_round(self):
        self.reset_deck()  # Reset the deck at the beginning of each round
        self.deal_hole_cards()
        self.deal_community_cards(5)
        # self.print_state()

        

        # Determine the winner
        winner = self.determine_winner()
        cprint("The Winner is Player " + str(winner))

        # Record the result for each player
        for i in range(self.num_players):
            first_card_value = self.player_hands[i][0].value
            second_card_value = self.player_hands[i][1].value

            if i + 1 == winner:
                result = "win"
            else:
                result = "loss"

            self.record_result(result, first_card_value, second_card_value)
    def save_frequencies(self):
        file_path = "all_hands_frequencies.json"
        with open(file_path, "w") as json_file:
            json.dump(self.all_hands_frequency, json_file)

def simulate():
    num_rounds = 100
    accumulated_total_wins = np.zeros((13, 13))
    accumulated_total_losses = np.zeros((13, 13))
    accumulated_winning_hand_frequency = {
        "Royal Flush": 0,
        "Straight Flush": 0,
        "Four of a Kind": 0,
        "Full House": 0,
        "Flush": 0,
        "Straight": 0,
        "Three of a Kind": 0,
        "Two Pair": 0,
        "One Pair": 0,
        "High Card": 0,
    }

    for num_players in range(2, 9):

        total_wins = np.zeros((13, 13))
        total_losses = np.zeros((13, 13))

        for i in range(num_rounds):
            texas_holdem_game = TexasHoldem(num_players)
            texas_holdem_game.play_round()

            total_wins += np.array(texas_holdem_game.wins_frequency)
            total_losses += np.array(texas_holdem_game.losses_frequency)
            print(str(num_players) + ": " + str(i) + "/" + str(num_rounds))

        accumulated_total_wins += total_wins
        accumulated_total_losses += total_losses

        cprint(f"\nResults for {num_players} players after {num_rounds} rounds:")
        cprint("\nWins Frequency:")
        for row in total_wins:
            cprint(row)

        cprint("\nLosses Frequency:")
        for row in total_losses:
            cprint(row)
        accumulated_winning_hand_frequency = {
            key: accumulated_winning_hand_frequency[key] + texas_holdem_game.winning_hand_frequency[key] for key in
            accumulated_winning_hand_frequency}

        np.savetxt(f"wins/wins_{num_players}_players_{num_rounds}_rounds.txt", total_wins)
        np.savetxt(f"losses/losses_{num_players}_players_{num_rounds}_rounds.txt", total_losses)

        # Save frequencies of all hands
        texas_holdem_game.save_frequencies()

    file_path = f"frequencies_{num_rounds}_rounds.json"
    with open(file_path, "w") as json_file:
        json.dump(accumulated_winning_hand_frequency, json_file)

    accumulated_total_wins = accumulated_total_wins
    accumulated_total_losses = accumulated_total_losses
    np.savetxt(f"wins/accumulated_wins_{num_rounds}_rounds.txt", accumulated_total_wins)
    np.savetxt(f"losses/accumulated_losses_{num_rounds}_rounds.txt", accumulated_total_losses)

def draw_probabilities(cards):
    probabilities = {
        "Royal Flush": 0,
        "Straight Flush": 0,
        "Four of a Kind": 0,
        "Full House": 0,
        "Flush": 0,
        "Straight": 0,
        "Three of a Kind": 0,
        "Two Pair": 0,
        "One Pair": 0,
        "High Card": 0,
    }

    rank_mapping = {
            10: "Royal Flush",
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card",
        }
    deck = Deck()
    deck.cards = [card for card in deck.cards if all(card.name != other_card.name for other_card in cards)]
    i = 0
    for card1 in deck.cards:
        for card2 in deck.cards:
            if card1 != card2:
                temp_cards = cards + [card1 , card2]
                rank, _ = rank_hand(temp_cards)
                probabilities[rank_mapping[rank]] += 1
                i+=1

    for key in probabilities:
        probabilities[key] /= i

    return probabilities

def test_evaluator():
    
    texas_holdem_game = TexasHoldem(3)
    texas_holdem_game.reset_deck()  # Reset the deck at the beginning of each round
    texas_holdem_game.deal_hole_cards()
    texas_holdem_game.deal_community_cards(5)

    for i in texas_holdem_game.community_cards:
        print(str(i), end=', ')
    print()
    print(draw_probabilities(texas_holdem_game.community_cards))
    print()
    cards = [Card("Jack","red", "Heart"), Card("10","red", "Heart"), Card("Ace", "red", "Heart"),Card("King", "red", "Heart"),Card("Queen", "red", "Heart")]

    texas_holdem_game.reset_deck()  # Reset the deck at the beginning of each round
    texas_holdem_game.deal_hole_cards()
    texas_holdem_game.deal_community_cards(4)

    for i in texas_holdem_game.community_cards:
        print(str(i), end=', ')
    print()
    print(draw_probabilities(texas_holdem_game.community_cards))
    print()
    cards = [Card("Jack","red", "Heart"), Card("10","red", "Heart"), Card("Ace", "red", "Heart"),Card("King", "red", "Heart"),Card("Queen", "red", "Heart")]

    texas_holdem_game.reset_deck()  # Reset the deck at the beginning of each round
    texas_holdem_game.deal_hole_cards()
    texas_holdem_game.deal_community_cards(3)

    for i in texas_holdem_game.community_cards:
        print(str(i), end=', ')
    print()
    print(draw_probabilities(texas_holdem_game.community_cards))
    print()
    cards = [Card("Jack","red", "Heart"), Card("10","red", "Heart"), Card("Ace", "red", "Heart"),Card("King", "red", "Heart"),Card("Queen", "red", "Heart")]



    for i in cards:
        print(str(i), end=' ')
    print()

    print(draw_probabilities(cards))



if __name__ == "__main__":
    simulate()

    # test_evaluator()

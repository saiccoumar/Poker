import sys
# Import deck from parent directory
# sys.path.append("../")

from .deck import *
from collections import Counter


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

class Player:
    def __init__(self, player_number, chips=100):
        self.chips = chips
        self.hand = []
        self.player_number = player_number

class TexasHoldem:
    
    def __init__(self, num_players=2):
        # Initialize Deck, players hands, community cards
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.player_hands = {player: [] for player in range(1, num_players + 1)}
        self.round = ""
        self.winning_rank = ""
        self.all_in = False


        # Initialize players  
        self.num_players = num_players
        self.players = {player: Player(player, chips=100*player) for player in range(1, num_players + 1)}
        self.dealer = 1
        self.current_player = (self.dealer % self.num_players) + 1
        
        self.players_in_round = {player: True for player in range(1, num_players + 1)}

        # Initialize bets
        self.cum_bets = {player: 0 for player in range(1, num_players + 1)}
        self.bets = {player: -1 for player in range(1, num_players + 1)}
        self.current_bet = 0
        self.pot = 0

        
    def reset_deck(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.player_hands = {player: [] for player in range(1, self.num_players + 1)}
        self.set_round("Pre-flop")
        self.winning_hand = ""
        self.all_in = False
        self.players_in_round = {player: self.players[player].chips != 0 for player in range(1, self.num_players + 1)}

    def reset_players(self):
        for _, player in self.players.items():
            player.hand = []
    
    def reset_bets(self):
        self.bets = {player: -1 for player in range(1, self.num_players + 1)}
        self.current_player = (self.dealer % self.num_players) + 1
        self.current_bet = 0

    def reset_pot(self):
        self.pot = 0
        self.current_bet = 0
        self.bets = {player: -1 for player in range(1, self.num_players + 1)}

    def set_round(self, round):
        self.round = round

    def get_game_state(self, player_num):
        """
        Get the game state for a specific player.

        Parameters:
        - player_num (int): The player number.

        Returns:
        - dict: The game state for the specified player.
        """
        player_state = {
            "round": self.round,
            "player_hand": [str(card) for card in self.player_hands[player_num]],
            "community_cards": [str(card) for card in self.community_cards],
            "current_bet": self.current_bet,
            "pot": self.pot,
            "current_player": self.current_player,
            "current_dealer": self.dealer,
            "bets": self.bets,
            "cum_bets": self.cum_bets,
            "chips": {player.player_number: player.chips for player in self.players.values() },
            "probabilities": self.draw_probabilities(self.community_cards)
        }

        return player_state
    def get_showdown_game_state(self):
        """
        Get the game state for a specific player.

        Parameters:
        - player_num (int): The player number.

        Returns:
        - dict: The game state for the specified player.
        """
        player_state = {
            "round": self.round,
            "players_hand": {player_num: [str(card) for card in self.player_hands[player_num]] for player_num in self.players.keys()},
            "community_cards": [str(card) for card in self.community_cards],
            "winner": self.determine_winner(),
            "pot": self.pot,
            "rank": self.winning_rank,
            "chips": {player.player_number: player.chips for player in self.players.values() }
        }

        return player_state

    def deal_hole_cards(self):
        for _ in range(2):
            for _ , hand in self.player_hands.items():
                hand.append(self.deck.deal_card())
        

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            self.community_cards.append(self.deck.deal_card())

    def determine_winner(self):
        all_hands = [hand + self.community_cards for hand in self.player_hands.values()]

        best_hands = [rank_hand(player_hand) for player_hand in all_hands]

        

        # Sort the best hands by rank and then by the highest card value
        sorted_best_hands = sorted(enumerate(best_hands), key=lambda x: (x[1][0], x[1][1]), reverse=True)

        # Determine the winner
        winner_key = list(self.player_hands.keys())[sorted_best_hands[0][0]]  # Get the key of the first (highest) hand
        winning_hand = all_hands[sorted_best_hands[0][0]]

        # Update winning_hand_frequency dictionary based on the hand rank
        rank, _ = best_hands[sorted_best_hands[0][0]]
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
        print("Winning Hand:" + rank_mapping[rank] + " with rank " + str(rank))
        self.winning_rank = rank_mapping[rank]
        print("| ", end="")
        for i in winning_hand:
            print(i.print_card(),end =" | ")
        print()

        return winner_key

    def place_bet(self, player_number, bet_amount):
        self.players[player_number].chips -= bet_amount
        self.pot += bet_amount
        self.bets[player_number] += bet_amount
        self.cum_bets[player_number] += bet_amount
        if (not self.all_in):
            self.current_bet = max(self.bets.values())
    
    def give_winnings(self, player_num):
        self.players[player_num].chips += self.pot
        self.pot = 0

    
    def switch_player(self):
        self.current_player = (self.current_player % self.num_players) + 1
        
    @staticmethod
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

    def check_bets_matched(self):
        if (max(self.bets.values()) < 0):
            return False
    # Iterate through players still in the round
        for player_num, in_round in self.players_in_round.items():
            if in_round:
                # Check if the player's bet matches the current bet
                if self.bets[player_num] < self.current_bet:
                    return False
        # If all players' bets match the current bet, return True
        return True  
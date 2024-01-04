from deck import *

class Blackjack:
    def __init__(self, num_players=1, num_decks=1):
        self.deck = self.create_deck(num_decks)
        self.deck.shuffle()
        self.num_players = num_players
        self.player_hands = [[] for _ in range(num_players)]
        self.dealer_hand = []

    def create_deck(self, num_decks):
        combined_deck = Deck()
        for _ in range(num_decks - 1):
            combined_deck = combine_decks(combined_deck, Deck())
        return combined_deck

    def deal_initial_cards(self):
        for _ in range(2):
            for hand in [self.dealer_hand] + self.player_hands:
                hand.append(self.deck.deal_card())

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0

        for card in hand:
            if card.name in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.name == 'Ace':
                value += 11
                num_aces += 1
            else:
                value += int(card.name)

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

    def play_round(self):
        self.deal_initial_cards()

        for i in range(self.num_players):
            print(f"Player {i + 1}'s turn:")
            while True:
                print(f"Your hand: {[str(card) for card in self.player_hands[i]]}, Value: {self.calculate_hand_value(self.player_hands[i])}")
                action = input("Do you want to hit or stand? ").lower()
                if action == 'hit':
                    self.player_hands[i].append(self.deck.deal_card())
                    if self.calculate_hand_value(self.player_hands[i]) > 21:
                        print("Bust! You went over 21.")
                        break
                elif action == 'stand':
                    break
                else:
                    print("Invalid action. Please enter 'hit' or 'stand'.")

        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.deal_card())

        print("\nFinal Results:")
        print(f"Dealer's hand: {[str(card) for card in self.dealer_hand]}, Value: {self.calculate_hand_value(self.dealer_hand)}")

        for i in range(self.num_players):
            print(f"Player {i + 1}'s hand: {[str(card) for card in self.player_hands[i]]}, Value: {self.calculate_hand_value(self.player_hands[i])}")

if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    num_decks = int(input("Enter the number of decks: "))
    game = Blackjack(num_players, num_decks)
    game.play_round()
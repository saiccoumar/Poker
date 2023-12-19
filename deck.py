import random

class Card:
    def __init__(self, name, color, suit):
        self.name = name
        self.color = color
        self.suit = suit
        self.value = self.calculate_poker_value()

    def calculate_blackjack_value(self):
        if self.name in ['Jack', 'Queen', 'King']:
            return 10
        elif self.name == 'Ace':
            return 1
        else:
            return int(self.name)
    def calculate_poker_value(self):
        if self.name == 'Jack':
            return 11
        elif self.name == 'Queen':
            return 12
        elif self.name == 'King':
            return 13
        elif self.name == 'Ace':
            return 14
        else:
            return int(self.name)

    def __str__(self):
        return f"{self.name} of {self.suit} ({self.color})"
    
    def print_card(self):
        return f"{self.name} of {self.suit} ({self.color})"
class Deck:
    def __init__(self):
        self.cards = []
        self.populate_deck()

    def populate_deck(self):
        names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        suits = ['Diamond', 'Clover', 'Spade', 'Heart']

        for suit in suits:
            for name in names:
                color = 'red' if suit in ['Diamond', 'Heart'] else 'black'
                card = Card(name, color, suit)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            print("No more cards in the deck.")
            return None

def combine_decks(deck1, deck2):
    combined_deck = Deck()
    combined_deck.cards = deck1.cards + deck2.cards
    return combined_deck

   
if __name__ == "__main__":
    deck1 = Deck()
    deck2 = Deck()

    # deck1.shuffle()
    deck2.shuffle()

    combined_deck = combine_decks(deck1, deck2)

    print("Deck:")
    for _ in range(52):
        card = deck1.deal_card()
        if card:
            print(card)

# client.py
import sys
# Import deck from parent directory
import socket
import json
from .poker_host import Player
from .deck import Card


"""
Limp Agent:
    This agent participates based on the concept of "limping" through games. Essentially, the agent will simply match bets so that it can stay in the game but not increase bets to try and gain an advantage. 
    In the poker community, this is quite looked down upon. It kills the excitement of the game and becomes "predictable" and drags on games where players with bad hands should fold. 
    This is a perfect default agent for our purposes! It's strategically weak, extremely easy to implement, and if bugs are thrown I know that it's not because of internal logic. 
Decision Making Logic:
    The decision making function will return 1 every time to call every hand. 
"""
class LimpAgent:
    def __init__(self):
        # initialize cliennt socket with localhost ip address on port 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.client_socket.connect((self.host, self.port))
        self.player_number = int(self.client_socket.recv(1024).decode())
        self.player = Player(self.player_number)
        self.player.chips *= self.player_number
        print(f"You are Player {self.player_number}")

    # Client messages Server
    def send_message(self, message):
        message = str(message)
        self.client_socket.send(message.encode())

    # Server messages Client
    def receive_data(self):
        data = self.client_socket.recv(1024).decode()
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    # Logic to play the game 
    def play_game(self):
        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False
        def is_str(value):
            try:
                str(value)
                return True
            except ValueError:
                return False
            
        while True:
            game_state = self.receive_data()
            # Wait for start code
            if isinstance(game_state, str) and game_state == "GAME STARTED":
                print("Game has started!")
                
            
            # Big Blind
            elif isinstance(game_state, str) and ("BIG" in game_state):
                self.player.chips -= 2
                # TODO: Handle when player cannot afford big blind
                if (self.player.chips < 0):
                    self.player.chips = 0
                
            # Small Blind
            elif isinstance(game_state, str) and ("SMALL" in game_state):
                self.player.chips -= 1
            
            # Server gives chips back to player
            elif isinstance(game_state, str) and ("GIVE" in game_state):
                first_tilde_pos = game_state.find("~")
                second_tilde_pos = game_state.find("~", first_tilde_pos + 1)
                # Extract the value between the tilde characters
                if first_tilde_pos != -1 and second_tilde_pos != -1:
                    chips = game_state[first_tilde_pos + 1:second_tilde_pos]
                    self.player.chips += int(chips)
                    print(f"You got {chips} chips back!")
                else:
                    print("Tilde characters not found or value not present.")
                
            # If the data is the cards make bets
            elif isinstance(game_state, dict):
                self.player.chips = game_state['chips'][str(self.player_number)]
                # print(f"Round: {game_state['round']}")
                if (game_state['round'] == 'Showdown!'):
                    self.print_showdown_cards(game_state)
                    if self.player.player_number == game_state['winner']:
                        self.player.chips += int(game_state['pot'])
                    chips_str = "\033[92m{}\033[0m".format(str(self.player.chips))
                    print(f"You now have {chips_str} chips!")
                    continue

                # Add cards into players hands if hand is empty 
                if len(self.player.hand) == 0:
                    for card_str in game_state["player_hand"]:
                        card = Card.from_str(card_str)
                        self.player.hand.append(card)

                print("\nCurrent Cards:")
                self.print_cards(game_state)
                # Active player makes their move
                if game_state['current_player'] == self.player_number:
                    # Game Info
                    print(f"Current Player: Player {game_state['current_player']}", end=" | ")
                    print(f"Current Dealer: Player {game_state['current_dealer']}", end=" | ")
                    print(f"Current Pot: {game_state['pot']}")
                    chips_str = "\033[92m{}\033[0m".format(str(self.player.chips))
                    print(f"You have {chips_str} chips")
                    if (game_state['current_bet'] == 0): 
                        print("What would you like to do?\nType 1 to check, 2 to raise, and 3 to fold")
                    if (game_state['current_bet'] > 0): 
                        print("What would you like to do?\nType 1 to call, 2 to raise, and 3 to fold")
                    print("Bets:")
                    print("| ",end="")
                    for player,bet in game_state['bets'].items():
                        if bet < 0:
                            bet = 0
                        print(f"Player {player}: {bet} chips", end=" | ")
                    print(f"Current Bet: {game_state['current_bet']} |")

                    # Get players choice
                    action, bet = self.make_decision(game_state=game_state)
                    # while ((not is_int(action)) or (int(action) < 1) or (int(action) > 3)):
                    #     print("Invalid choice.")
                    #     action = self.make_decision(game_state=game_state)
                    
                    self.send_message(action)
                    # TODO: Handle when player cannot bet but tries to anyways
                    if int(action) == 2:
                        
                        # Player cannot make bet if the bet is not a number, 
                        while ((not is_int(bet)) or (int(bet) < 0) or ((int(bet) + game_state['current_bet']) > self.player.chips)):
                            print("Invalid bet.")
                            raise Exception("Invalid Bet has occurred from automated bot")
                        self.player.chips -= int(bet) + game_state['current_bet']
                        self.send_message(bet)

                    # Action should always be 1
                    if int(action) == 1:
                        print("AI Called!!!")
                        if game_state['bets'][str(self.player.player_number)] >= 0:
                            self.player.chips += game_state['bets'][str(self.player.player_number)]
                            self.player.chips -= int(game_state['current_bet'])
                            
                    print()
                else:
                    print("Waiting for the other player's move...")
            # If the move is invalid, the player is prompted again
            elif isinstance(game_state, str) and game_state == "INVALID_MOVE":
                print("Invalid move. Please try again.")
                continue
            
            elif isinstance(game_state, str) and ("WIN" in game_state):
                print("Congratulations! You won!")
                self.player.hand = []

                action = input("Do you want to play again? (y/n)")
                action = action.lower()
                while not is_str(action) or (action != "y" and action != "n"):
                    print('invalid entry')
                    action = input("Do you want to play again? (y/n)")
                    action = action.lower()
                self.send_message(action)
                
            elif isinstance(game_state, str) and ("LOSS" in game_state):
                print("Sorry, you lost...")
                self.player.hand = []
                
                action = input("Do you want to play again? (y/n)")
                action = action.lower()
                while not is_str(action) or (action != "y" and action != "n"):
                    print('invalid entry')
                    action = input("Do you want to play again? (y/n)")
                    action = action.lower()
                self.send_message(action)
                
            # Break code when the game ends
            elif isinstance(game_state, str) and ("END" in game_state):
                print("Game ended.")
                break
            elif isinstance(game_state, str):
                print(game_state)
                
    # Close client socket
    def close_connection(self):
        self.client_socket.close()

    @staticmethod
    def make_decision(game_state):
        # Shoutout raiden. You'd be so proud. 
        return 1, 0
    

    # Helper methods for formatting
    @staticmethod
    def print_cards(game_state):
        print(f"Your Hand:")
        print("| ", end="")
        for card_str in game_state["player_hand"]:
            card = Card.from_str(card_str)
            print(card.print_card(),end = " | ")
        print("\n---------------------------")
        if (len(game_state['community_cards']) > 0):
            print(f"Community Cards:")
            print("| ", end="")
            for card_str in game_state["community_cards"]:
                card = Card.from_str(card_str)
                print(card.print_card(),end = " | ")
        print()
    @staticmethod
    def print_showdown_cards(game_state):
        for player, hand in game_state['players_hand'].items():
            print(f"Player {player}'s Hand:")
            print("| ", end="")
            for card_str in hand:
                card = Card.from_str(card_str)
                print(card.print_card(),end = " | ")
            print("\n---------------------------")
        if (len(game_state['community_cards']) > 0):
            print(f"Community Cards:")
            print("| ", end="")
            for card_str in game_state["community_cards"]:
                card = Card.from_str(card_str)
                print(card.print_card(),end = " | ")
        print()
        


        

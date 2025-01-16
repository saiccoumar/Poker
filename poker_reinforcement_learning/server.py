# server.py

import socket
import threading
from .poker_host import Player, TexasHoldem
import json
import time

class ServerPlayer(Player):
    def __init__(self, player_number, chips=100, client_socket=None):
        super().__init__(player_number, chips)
        # ServerPlayer info is redundant, really only need the player_number and client_socket
        self.client_socket = client_socket

# Server Class
class Server:
    def __init__(self,num_players):
        # initialize server socket with localhost ip address on port 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(num_players)
        print("Server is listening for connections...")
        # Array for player socket
        self.players = {}
        # Game imported from poker_host
        self.game = TexasHoldem(num_players)
        self.num_players = num_players
        self.num_players_connected = 0
        self.lock = threading.Lock()
        self.dealer_check_event = threading.Event()
        # Players Recieved Message Counter
        self.prm = 0
        # Condition to play more rounds of poker
        self.keep_playing = True
        # Keeps track of players leaving
        self.players_connected = True
        

    # Function to send game state from the server to the client. Game state includes the board information as well as whose turn it is. Game state info is in json format
    def send_game_state(self, player):
        game_state = self.game.get_game_state(player.player_number)
        json_data = json.dumps(game_state)
        print(f"Sending game state to Player {player.player_number}: {json_data}")
        player.client_socket.send(json_data.encode())

    def reset_thread_management(self):
        self.lock = threading.Lock()
        self.dealer_check_event = threading.Event()
    
    # PRM: Players recieved message. Reset to 0 for new message
    def reset_prm_counter(self):
        self.prm = 0

    def send_game_state_to_all(self):
        for _ , player in self.players.items():
            self.send_game_state(player)
    
    def send_global_message(self, message):
        for _ , player in self.players.items():
            player.client_socket.send(str(message).encode())
    
    def check_for_early_win(self):
        return list(self.game.players_in_round.values()).count(True) == 1
    
    def get_early_winner(self):
        for key, value in self.game.players_in_round.items():
            if value is True:
                return key

    def round(self, name):

        # all_in() checks for bet_amounts that empty a players chips 
        def all_in(player, bet_amount):
            # Get the players chips
            temp_chips = self.game.get_game_state(player.player_number)['chips'][player.player_number]
            
            # Check if the bet is too large
            if ((temp_chips - bet_amount) <= 0):
                print(f"player: {player.player_number}")
                print(f"chips: {temp_chips}")
                print(f"bet flag: {bet_amount}") 

                # Player puts in all their chips 
                bet_amount = temp_chips
                print(f"Player {player.player_number} is ALL IN!.")
                self.send_global_message(f"Player {player.player_number} is ALL IN!.")
                self.game.all_in = True
                # current bet is the amount of chips they can bet + the chips they already bet = all their chips
                self.game.current_bet = bet_amount + self.game.bets[player.player_number]
                # Give back chips from side pot
                # Fix Current pot
                for player_number , other_player_bet in self.game.bets.items():
                    if other_player_bet > self.game.current_bet:
                        # Calculate the difference between the current bet and the players bets that are higher
                        diff = other_player_bet - self.game.current_bet
                        print(f"Diff: {diff}")
                        # Give back chips that go over current bet
                        self.game.cum_bets[player_number] -= diff
                        self.game.players[player_number].chips += diff
                        other_player_bet = self.game.current_bet
                        self.players[player_number].client_socket.send(str(f"GIVE~{diff}~").encode())
                        print(f"Gave player {player_number} {diff} chips")
                
            return bet_amount

        self.game.round = name
        self.send_global_message(f"-----------------------------------------------------------------------\n{name} Round")
        self.game.set_round(name)
        print(f"\nRound Called: {name}")
        # Big/Small Blind 
        if (name == "Pre-flop"):
            for i in range(2,0,-1):  
                player = self.players[self.game.current_player]
                if (self.game.bets[player.player_number] < 0):
                    self.game.bets[player.player_number] = 0
                self.game.place_bet(player.player_number, i)
                # Notify players of bets
                if i == 1:
                    print(f"Player {player.player_number} placed the small blind.")
                    self.send_global_message(f"Player {player.player_number} placed the small blind.")
                    player.client_socket.send("SMALL".encode())
                else:
                    print(f"Player {player.player_number} placed the big blind.")
                    self.send_global_message(f"Player {player.player_number} placed the big blind.")
                    player.client_socket.send("BIG".encode())
                self.game.switch_player()
            
        # Check if betting needs to continue
        while(not self.game.check_bets_matched()):
            # Set the current player
            player = self.players[self.game.current_player]
            if (self.game.bets[player.player_number] < self.game.current_bet):
                # Send all users game state. The current player will be the only one who can interact
                self.send_game_state_to_all()

                # If the player folded, pass them
                if self.game.players_in_round[player.player_number] == True:
                    
                    # Get the active players choice
                    action = player.client_socket.recv(1024).decode()
                    if action == "1":  # Check/Call
                        if (self.game.bets[player.player_number] < 0):
                            self.game.bets[player.player_number] = 0
                        if(self.game.bets[player.player_number] == self.game.current_bet):
                            print(f"Player {player.player_number} checks.")
                            self.send_global_message(f"Player {player.player_number} checks.")
                        else:
                            print(f"Player {player.player_number} calls.")
                            self.send_global_message(f"Player {player.player_number} checks.")

                        bet_amount = self.game.current_bet - self.game.bets[player.player_number]


                        # All in   
                        bet_amount = all_in(player, bet_amount)

                                    
                        print(f"Player {player.player_number} bets {bet_amount} chips.")
                        self.game.place_bet(player.player_number, bet_amount)
                    elif action == "2":  # Raise Bet
                        if (self.game.bets[player.player_number] < 0):
                            self.game.bets[player.player_number] = 0
                        bet_amount = int(player.client_socket.recv(1024).decode()) + self.game.current_bet
                         
                        # All in     
                        bet_amount = all_in(player, bet_amount)

                        self.game.place_bet(player.player_number, bet_amount)
                        print(f"Player {player.player_number} bets {bet_amount} chips.")
                        self.send_global_message(f"Player {player.player_number} bets {bet_amount} chips.")
                        
                    elif action == "3":  # Fold
                        print(f"Player {player.player_number} folds.")
                        self.send_global_message(f"Player {player.player_number} folds.")
                        self.game.players_in_round[player.player_number] = False
                        # self.players[i].hand = []  # Remove player's hand
                    else: # Theoretically never gets called
                        print("Invalid choice. Please choose again.")
                    print(f"Bets matched: {self.game.check_bets_matched()}")
                    print(f"Bets: {self.game.bets}")
                    print(f"Early Win Detected: {self.check_for_early_win()}")
                    

                    if (self.game.check_bets_matched()):
                        break
                    if (self.check_for_early_win()):
                        winner = self.get_early_winner()
                        print(f"Winner (by betting): {winner}")
                        # self.send_global_message("END")
                        break
                    else:  
                        self.game.switch_player()
                        print(f"Current Player: {self.game.current_player}")
                        # self.send_game_state(self.players[self.game.current_player])
                    print('\n')
                else:
                    pass
            else:
                self.game.switch_player()
            # if (self.game.check_bets_matched()):
            #     break
    # Logic that the server runs to interact with the clients and handle game management
    def handle_client(self, player):
        def keep_playing_game(client_socket):
            with self.lock:
                self.game.reset_bets()
                self.game.reset_players()
                self.game.reset_deck()
                self.game.reset_pot()
                print(f"Player has sent their response")
                answer = client_socket.recv(1024).decode()
                print(f"Answer: {answer}")
                if str(answer) == "n":
                    print("Game Ending.")
                    self.keep_playing = False
            time.sleep(0.1)  
                
        
        def game_ended_early(player_number):
            # Determine who won
            winner = None
            for key, value in self.game.players_in_round.items():
                if value == True:
                    winner = key
                    break
            
            pot = self.game.pot
            # print(f"pot: {pot}")
            # Send showdown information for client to display
            if (player_number == self.game.dealer):
                
                print(f"Player {winner} has won!")
                self.send_global_message(f"All other players have folded. Player {winner} has won {pot} chips!")
                self.game.give_winnings(winner)
                
                for player_num , player in self.players.items():  
                    if (player_num == winner):
                        player.client_socket.send(str(f"GIVE~{pot}~\n").encode())
                        time.sleep(0.1)
                        player.client_socket.send(str("WIN").encode())
                    else:
                        time.sleep(0.1)
                        player.client_socket.send(str("LOSS").encode())
                self.game.dealer = (self.game.dealer % self.game.num_players) + 1
                self.reset_prm_counter()

        
        client_socket = player.client_socket
        player_number = player.player_number
        
        client_socket.send(str(player_number).encode())

        # Wait for 2 players before interacting with the client further   
        while self.num_players_connected != self.game.num_players:
            pass
 

        # With self.lock, .set(), .wait(), .clear() used to lock threads so all players catch up after rounds
        while self.keep_playing:
            # Send game start code

            with self.lock:
                client_socket.send("GAME STARTED".encode())
                self.prm+=1
                print(f"PRM: {self.prm}, Num Players: {self.num_players_connected}")
                if (self.prm==self.num_players_connected):
                    self.reset_prm_counter()
                self.dealer_check_event.set()
            self.dealer_check_event.wait()
            self.dealer_check_event.clear()

            print("Checkpoint 1")
            
            # Pre-flop round
            with self.lock:
                if player_number == self.game.dealer:
                    self.game.deal_hole_cards()

                    self.round("Pre-flop")
                    print("Pre-Flop Betting Ended")
                    self.send_global_message("Pre-Flop Betting Ended")
                    self.game.deal_community_cards(3)
                    self.game.reset_bets()
                    self.dealer_check_event.set()

            self.dealer_check_event.wait()
            self.dealer_check_event.clear()    

            print("Checkpoint 2")
            
            # Flop round
            if not self.check_for_early_win():
                with self.lock:
                    if player_number == self.game.dealer:
                        if (not self.game.all_in):
                            self.round("Flop")
                            print("Flop Betting Ended")
                            self.send_global_message("Flop Betting Ended")
                        self.game.deal_community_cards(1)
                        self.game.reset_bets()
                        print(self.game.bets)
                    self.dealer_check_event.set()
                self.dealer_check_event.wait()
                self.dealer_check_event.clear()
            else:
                game_ended_early(player_number)
                keep_playing_game(client_socket)
                continue

            print("Checkpoint 3")

            # Turn round
            
            if not self.check_for_early_win():
                with self.lock:
                    if player_number == self.game.dealer: 
                        if (not self.game.all_in):
                            self.round("Turn")
                            print("Turn Betting Ended")
                            self.send_global_message("Turn Betting Ended")
                        self.game.deal_community_cards(1)
                        self.game.reset_bets()
                        print(self.game.bets)
                    self.dealer_check_event.set()
                self.dealer_check_event.wait()
                self.dealer_check_event.clear()
            else:
                game_ended_early(player_number)
                keep_playing_game(client_socket)
                continue                
                
            print("Checkpoint 4")
            
            # River round
            if not self.check_for_early_win():
                with self.lock:
                    if player_number == self.game.dealer:
                        if (not self.game.all_in):
                            self.round("River")
                            print("River Betting Ended")
                            self.send_global_message("River Betting Ended")
                        self.game.reset_bets()
                        print(self.game.bets)
                    self.dealer_check_event.set()
                self.dealer_check_event.wait()
                self.dealer_check_event.clear()
            else:
                game_ended_early(player_number)
                keep_playing_game(client_socket)
                continue

            print("Checkpoint 5\n")

            # SHOWDOWN            
            with self.lock:
                if player_number == self.game.dealer:
                    print("Showdown!")
                    self.game.set_round("Showdown!")
                    self.send_global_message("Showdown!")

                    # Determine who won
                    winner = self.game.determine_winner()
                    print(f"Player {winner} has won!")
                    game_state = self.game.get_showdown_game_state()
                    self.game.give_winnings(winner)

                    # Send showdown information for client to display
                    self.send_global_message(f"Player {winner} has won {game_state['pot']} chips! with a {game_state['rank']}")
                    for player_num , player in self.players.items():
                        json_data = json.dumps(game_state)
                        print(f"Sending showdown game state to Player {player.player_number}: {json_data}")
                        player.client_socket.send(json_data.encode())    
                        if (player_num == winner):
                            player.client_socket.send(str("WIN").encode())
                        else:
                            player.client_socket.send(str("LOSS").encode())
                self.dealer_check_event.set()

            print("Checkpoint 6")
            
            self.dealer_check_event.wait()
            self.dealer_check_event.clear()

            keep_playing_game(client_socket)


            # If only one player has chips end the game
            if self.check_for_early_win():
                print("Only one player has chips. Game ending now.")
                self.send_global_message("Only one player has chips. Game ending now.")
                break
        


        # Close connection to client when the game is over
        try:
            self.send_global_message("END")
        finally:
            print(f"Connection from {client_socket.getpeername()} has been closed.")
            client_socket.close()
            self.players_connected = False

    def accept_connections(self):
        # Repeatedly check for clients that will join
        while self.players_connected and self.num_players_connected < self.num_players:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")
            # Add clients to players array for reference later
            self.num_players_connected += 1
            player = ServerPlayer(self.num_players_connected, chips=100*self.num_players_connected, client_socket = client_socket)
            self.players[self.num_players_connected] = player
            # Start a new threat for each client
            threading.Thread(target=self.handle_client, args=(player,)).start()

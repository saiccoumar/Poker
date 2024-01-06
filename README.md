# Poker ♡ ♣ ♢ ♠
<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/Poker/assets/55699636/e0613b16-97a4-43d3-970c-a5d1f1a20f35">
</p>

by Sai Coumar

# Introduction
Welcome to my python client/server implementation of Poker for use with Artificial Intelligence algorithms! This implementation is designed from scratch with Object-Oriented Programming principles for easy modularity in creating AI Agents and abstracted for interpretability. This repository also contains some code I wrote for statistical analysis as well as data I collected from simulations. I'll be covering the components of the project and technical aspects of development here, and cover a more in-depth write up about the AI algorithms I'll be implementing in the future over on my medium page. Stay tuned!

## Card
The first thing we need for a game of poker is obviously playing cards. In deck.py, I created the Card class with the properties name, suit, color, and value. Name, suit, and color are all initialized by the constructor, and value is determined based on the name of the card a helper method. Card games have different value systems for different cards, so this code can be repurposed with new helper methods that fit those rules. 

## Deck
Now that we have cards, we need to collect them into a deck. In deck.py I created the Deck Class which is a collection of cards and has a method to populate the deck, shuffle the cards, and deal cards from the deck. I also created a combine deck function while experimenting with blackjack. 

## Poker Simulations
My first iteration of this project was with poker_simulations.py. You can run this for yourself using the command:
```
python poker_simulations.py
```
poker_simulations.py uses a rudimentary ruleset of the game to generate simulated data of poker. I created the class TexasHoldEm, which has a deck, community cards, and the hands of each players. It also has the functionality to deal community cards and hole cards. This class has many methods, many of which are for recording data and managing the game, but there are two in particular to take note of.

***play_round()*** simulates a single round of poker. It resets the cards in the deck, shuffles them, and then deals 2 to each player and 5 onto the community cards; This effectively skips to the showdown round. 

***determine_winner()***, and it's helper method ***rank_hand()***, is the bread and butter of this program. determine_winner() evaluates the 2 cards each player + 5 community cards and then sorts them by their rank. It then returns the index of the hand that won. ***rank_hand()*** takes 7 cards, and then returns the rank of the best combination of 5 cards that can be made with those 5 cards. 

In poker there are 10 ranks, with the Royal flush being the highest (rank 10) and the high card being the lowest (rank 1). It also returns the value of the highest card, because if two hands have the same rank, the player with the higher card value wins. rank_hand() was tested extensively in tests.py, and I recommend checking the logic yourself if you're interested.
<p align="center">
  <img width="60%" height="auto" src="https://github.com/saiccoumar/Poker/assets/55699636/c83703ac-860c-4b66-bef3-3676b0e92ac9">
</p>
<p align="center">
  <em> https://www.poker.org </em>
 <em> I ranked mine with 1 as the lowest and 10 as the highest. This graphic reverses that.</em>
</p>
Also note that this is not the most efficient implementation of rank_hand(). In my research I found that bit-wise evaluations of hands were far more efficient for large scale poker applications on servers. 
   <br />

In the code, you can vary num_rounds and num_players to get the simulated data you desire.  

There is also a function, ***draw_probabilities()*** which calculates the probabilities of having a hand of a rank with 2 random cards (an opponents cards) given the community cards available. This was made in advance because such probabilities will be more useful when implementing the AI agents.. 
![evaluator_test](https://github.com/saiccoumar/Poker/assets/55699636/f3cd1263-12ea-4cc0-8f55-86751488ad87)

## Poker Game
The poker game has 3 subcomponents.
### Poker Host
Poker_host defines the class that creates an instance of TexasHoldEm. Poker_host is the second iteration built on the code used in poker_simulations.py. It contains properties for game management, ***draw_probabilities***, ***rank_hand()***, and ***determine_winner()*, as well as betting functionality. Also, it allows for game state information to be condensed into a JSON format which is extremely important for AI agents to have available to them.
### Server
Server runs TexasHoldEm and manages interactions with the clients in the game as well as the round based game logic. Each client is managed by a thread that runs handle_client(). One client, designated the dealer, executes the logic for game management (similar to how one player deals cards), and thread locking is used to enforce synchronization 
### Client
Client which allows a player to connect and play the game. Clients continuously wait for activation codes from the server, and respond when prompted to participate in the poker game. The Client also displays the game state info in the CLI as the UI for players to play the game with. 

## Important Technical Elements
### Threading
Unlike with Tic Tac Toe, much more threading logic was needed to make this game run. Each client gets their own thread in the server and both need to be synchronized or actions might get repeated. For example, if a function to give the pot to the winner is included in handle client once, and there are two players, it will give the pot winnings to the winner twice because both threads run the function once, totaling two function calls. 
```
with self.lock:
   #code
   self.event.set()
self.wait()
self.clear()
```
This block of code allowed me to set up checkpoints where both threads would need to synchronize before continuing on with the program. For example, the threads had to synchronize information after every round so that one client didn't start betting on the next round before the current round was complete. The way this code block works is that once a thread reaches wait() all of threads must trigger set() before any threads continue past wait(). Internally, set() sets a flag for the thread to true, wait() waits for all threads to have flags set to true, and clear() sets all the flags to false for the next checkpoint. 
### Game State
```
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
```

Using a game state to hold information and passing it from the server to the client was essential. It allowed for batch communications rather than sending individual messages at a time and will be vital for programming AI agents. Most AI algorithms are designed with the concept of a game_state that the AI interprets and acts upon. 
### Object-Oriented Programming
OOP design principles ensure that the code is extremely easy to follow and interpret. This project took me 5 separate attempts because when the design of the project started falling apart, it became increasingly difficult to detect and avoid bugs - especially with the client/socket configuration. This also ensures that when making AI agents, we'll be able to easily slot in new AI agents easily without needing to extensively rework the code base. I made this a priority after working on the Berkeley CS188 Pac-man projects in my coursework as I noticed that they took OOP principles and ran with it to abstract the actions. 

## Conclusion
Thank you for reading about my poker project! As of 01/05/2024, the game has been completed and the AI agents are still in development. Come back soon to see updates!



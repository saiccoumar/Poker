# Poker ♡ ♣ ♢ ♠
<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/Poker/assets/55699636/e0613b16-97a4-43d3-970c-a5d1f1a20f35">
</p>

by Sai Coumar

# Introduction
Welcome to my python client/server implementation of Poker for testing Artificial Intelligence algorithms! This implementation is designed from scratch with Object-Oriented Programming principles for easy modularity in creating AI Agents and abstracted for interpretability. I'll be covering relevant information to get this package up and running for efficiently testing different algorithms, the components of the project, technical aspects of development here, and exploring a basic statistical analysis @ .

## Installation
Currently, poker_rl is not available on pip. Install it by cloning the repository and running ```pip install -e .``` in the home directory to install the package in editable mode. Example scripts are included in the repository to test the code. poker_rl can then be imported into python code using ```import poker_rl```.

## Running a Poker Game

To run a game of poker, start the host server in a terminal with a parameter for however many agents (players) will be included in the game. The game will start when all players have joined the game. Add players by running agents in separate terminals. 

### Server
The host Server runs TexasHoldEm from Poker_Host and manages interactions with the clients in the game as well as the round based game logic. Each client is managed by a thread that runs handle_client(). One client, designated the dealer, executes the logic for game management (similar to how one player deals cards), and thread locking is used to enforce synchronization. An example of starting a server is included in start_server.py.
```
import argparse
import threading
from poker_rl import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Your program description here.')
    parser.add_argument('--num_players', type=int, default=2, nargs='?', const=2, choices=range(2, 9),
                    metavar='N', help='Number of players in the game (min=2, max=10)')
    # Start server and accept connections on a separate thread
    args = parser.parse_args()
    num_players = args.num_players
    server = Server(num_players)
    # Threading optional but included
    threading.Thread(target=server.accept_connections).start()

```
To start the server run
```
python start_server --N <n players>
```

### Agents
#### Client
Client which allows a human agent to connect and play the game. Clients continuously wait for activation codes from the server, and respond when prompted to participate in the poker game. The Client also displays the game state info in the CLI as the UI for players to play the game with. An example of creating a client is included in run_client.py.
```
from poker_rl import Client

if __name__ == "__main__":
    # Create a client that plays the game. When the game is over, close it's connection to the port.
    client = Client()
    client.play_game()
    client.close_connection()
    
```
To run the client run
```
python run_client.py
```

#### LimpAgent
LimpAgent is an automated agent that constantly calls/checks pots. This serves as a baseline model and represents a technique in poker known as "limping" where a player does not increase stake and plays through a hand with minimal risk to maximize playing time. It is generally considered a poor strategy and leads to less folding but has the potential to win some gains. This is a good baseline as we know it is a viable strategy to play the game and win sometimes, but not nearly optimal and can be drastically improved on. Instantiating a LimpAgent is very similar to a instantiating a human Client, and an example is provided in run_limp_agent.py.
```
from poker_rl import LimpAgent

if __name__ == "__main__":
    # Create a client that plays the game. When the game is over, close it's connection to the port.
    client = LimpAgent()
    client.play_game()
    client.close_connection()
    
```
To run the client run
```
python run_limp_agent.py
```

#### DummyAgent
Dummy agent provides a proxy to provide custom logic to an AI agent. A logic function is defined and passed in as a parameter for initializing a DummyAgent, and DummyAgent uses this logic function to make a decision when prompted with a given game state. An example of instantiating a DummyAgent with a custom logic function is included in run_folding_agent.py. The logic function used here is "immediately folding", where the agent decides the hand is too risky and immediately folds. Every time. 
```
from poker_rl import DummyAgent

def logic(game_state):
    print(game_state)
    print("\nNah, I don't want to play this hand")
    return 3, 0


if __name__ == "__main__":
    # Create a client that plays the game. When the game is over, close it's connection to the port.
    client = DummyAgent(logic=logic)
    client.play_game()
    client.close_connection()
```

A game state is provided as input to the custom logic function. The game state is a dictionary of relevant information about the current state of the game that informs the decision that the logic function may make. Below is an example of information included in the game_state:
```{'round': 'Flop', 'player_hand': ['4 of Diamond (red)', 'Queen of Heart (red)'], 'community_cards': ['7 of Clover (black)', '4 of Clover (black)', '2 of Heart (red)'], 'current_bet': 0, 'pot': 4, 'current_player': 2, 'current_dealer': 1, 'bets': {'1': -1, '2': -1}, 'cum_bets': {'1': 2, '2': 2}, 'chips': {'1': 98, '2': 198}, 'probabilities': {'Royal Flush': 0.0, 'Straight Flush': 0.0, 'Four of a Kind': 0.0, 'Full House': 0.0, 'Flush': 0.0, 'Straight': 0.0, 'Three of a Kind': 0.0, 'Two Pair': 0.0, 'One Pair': 0.07692307692307693, 'High Card': 0.9230769230769231}}```

Actions are encoded numerically:
- 1: Call/check bet
- 2: Raise the bet
- 3: Fold the hand.
The logic function must return a decision in the format of 
```
return action, bet
```
The bet value is ignored if the action is calling, checking, or folding. Exceptions will be thrown if improper input is passed in by an automated agent. 

Properties of the agent class can be accessed, but all of them only provide networking information. Game chips is included but can be accessed more easily through the game state dictionary.

## Foundational Classes:
### Card
The first thing we need for a game of poker is obviously playing cards. In deck.py, I created the Card class with the properties name, suit, color, and value. Name, suit, and color are all initialized by the constructor, and value is determined based on the name of the card a helper method. Card games have different value systems for different cards, so this code can be repurposed with new helper methods that fit those rules. 

### Deck
Now that we have cards, we need to collect them into a deck. In deck.py I created the Deck Class which is a collection of cards and has a method to populate the deck, shuffle the cards, and deal cards from the deck. I also created a combine deck function while experimenting with blackjack. 

### Poker Host
Poker_host defines the class that creates an instance of TexasHoldEm. Poker_host is the second iteration built on the code used in poker_simulations.py. It contains properties for game management, ***draw_probabilities***, ***rank_hand()***, and ***determine_winner()***, as well as betting functionality. Also, it allows for game state information to be condensed into a JSON format which is extremely important for AI agents to have available to them.

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

There is also a function, ***draw_probabilities()*** which calculates the probabilities of having a hand of a rank with 2 random cards (an opponents cards) given the community cards available. This was made in advance because such probabilities will be more useful when implementing the AI agents.. 
![evaluator_test](https://github.com/saiccoumar/Poker/assets/55699636/f3cd1263-12ea-4cc0-8f55-86751488ad87)


## Important Technical Elements

### Threading
Threading logic was needed to make this game run. Each client gets their own thread in the server and both need to be synchronized or actions might get repeated. For example, if a function to give the pot to the winner is included in handle client once, and there are two players, it will give the pot winnings to the winner twice because both threads run the function once, totaling two function calls. 
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
OOP design principles ensure that the code is extremely easy to follow and interpret. This project took me several attempts because when the design of the project started falling apart, it became increasingly difficult to detect and avoid bugs - especially with the client/socket configuration. This also ensures that when making AI agents, we'll be able to easily slot in new AI agents easily without needing to extensively rework the code base.
<!--
This agent is our default agent. Originally, I intended to make a randomized agent the default, similar to my Tic Tac Toe agent beforehand. But I thought back to a recent game of poker I played where someone exclusively called every hand. Regardless of hand strength - even if they knew they would lose - they refused to fold or bet higher. In poker, this strategy is called limping: you "limp" through the hand and bet the minimum required to stay in the game but refuse to fold so you can see your results on the flop while risking as little as possible. 

  As far as poker strategies go, this is one of the worst. When you win, you win small since you never increased the pot. Your chances of a loss are higher than most other strategies where you fold weaker hands, and losing drags out the game than if everyone with weak hands had folded early. It's also the perfect control strategy! It's strategically weak, extremely easy to implement, and if bugs are thrown I know that it's not because of internal decision making logic. -->

## Conclusion
Thank you for reading about my poker project! As of 01/05/2024, the game has been completed and the AI agents are still in development. Come back soon to see updates!

Update 1 (2/15/2023): Limp Agent has been added! 

#### Gallery:
<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/Poker/assets/55699636/4a3591a7-10c3-4364-a16d-face2a3cff61">
</p>
<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/Poker/assets/55699636/894bf6b3-a5e5-45fc-b738-bb1c19afbf5a">
</p>
<p align="center">
 <img size="100%" src="https://github.com/saiccoumar/Poker/assets/55699636/1f151d6c-b726-4de7-899f-16683ad42512">
</p>


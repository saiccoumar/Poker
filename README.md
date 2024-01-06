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
### Poker Host
### Client
### Server

## Important Technical Elements
### Threading
### Game State
### Object-Oriented Programming



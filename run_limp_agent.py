from poker_reinforcement_learning import LimpAgent



if __name__ == "__main__":
    # Create a client that plays the game. When the game is over, close it's connection to the port.
    client = LimpAgent()
    client.play_game()
    client.close_connection()
    
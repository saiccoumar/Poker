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
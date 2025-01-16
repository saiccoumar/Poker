import argparse
import threading
from poker_reinforcement_learning import Server

   
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

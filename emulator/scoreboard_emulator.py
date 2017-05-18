
import argparse

from scoreboard import Scoreboard
from virtual_scoreboard import VirtualScoreboard
from physical_scoreboard import PhysicalScoreboard

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser( description = 'Live baseball scoreboard emulator.' )
    arg_parser.add_argument('--team', action='store', default="Red Sox", type=str, help='')
    arg_parser.add_argument("-v", "--virtual", help="Run scoreboard in virtual mode.", action="store_true")
    args = arg_parser.parse_args()

    scoreboard = VirtualScoreboard() if args.virtual else PhysicalScoreboard()
    scoreboard.run()

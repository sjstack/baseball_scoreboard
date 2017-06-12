import time
import json
import requests
import logger as paul_bunyan

from game_data import *
from datetime import datetime, timedelta

DEFAULT_OPTS = {
    'debug': False,
    'virtual': True,
    'team': 'Red Sox'
}

class Scoreboard:
    def __init__( self ):
        self.running = False
        self.game_data = GameData()

    def run( self, opts = DEFAULT_OPTS ):
        self.opts     = opts
        self.running = True

        while self.running:
            if self.opts['debug']:
                self.run_()
            else:
                try:
                    self.run_()
                except Exception as ex:
                    paul_bunyan.log_exception( ex )

    def run_( self ):
        self.set_scoreboard_url()
        self.get_scoreboard_json()
        self.running = False

    def set_scoreboard_url( self, datetime = None ):
        if None == datetime:
            datetime = self.datetime_shift()
        year  = datetime.year
        month = datetime.month
        day   = datetime.day

        self.scoreboard_url = 'http://gd2.mlb.com/components/game/mlb/year_%04i/month_%02i/day_%02i/master_scoreboard.json' % (year, month, day)

    def datetime_shift( self, utc_datetime = datetime.utcnow(), hours_rewind=12 ):
        return utc_datetime - timedelta( hours=hours_rewind )

    def get_scoreboard_json( self ):
        response = requests.get( self.scoreboard_url )
        self.response_json = json.loads( response.content )
        self.game_json     = self.find_game_by_team( self.opts['team'] )

    def find_game_by_team( self, i_team_name ):
        games = []
        for game in self.response_json['data']['games']['game']:
            if game['home_team_name'] == i_team_name or game['away_team_name'] == i_team_name:
                games.append( game )
                if game['status']['status'] == "In Progress":
                    return game
        return games[-1]

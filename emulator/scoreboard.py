import os
import sys
import json
import requests

sys.path.append('./utils')
import logger as paul_bunyan
import time_utils

DEFAULT_ARGS = {
    'debug': False,
    'virtual': True,
    'team': 'Red Sox',
    'record': False,
    }

class Scoreboard:
    def __init__( self ):
        print 'init Scoreboard'
        self.mb_running = False

    def run( self, args = DEFAULT_ARGS ):
        self.set_runtime_params( args )

        self.game = GameState()
        self.mb_running = True
        while self.mb_running:
            if self.mb_debug_mode:
                self.run_()
            else:
                try:
                    self.run_()
                except Exception as ex:
                    paul_bunyan.log_exception( ex )
                    self.mb_running = False
                    return
            time.sleep( 5 )

    def set_runtime_params( self, i_runtime_args ):
        self.ms_team_name   = i_runtime_args['team']
        self.mb_debug_mode  = i_runtime_args['debug']
        self.mb_record_mode = i_runtime_args['record']

    def run_( self ):
        print "Running Scoreboard"
        response_json = self.request_gameday_data()
        game_json = self.find_game_by_team( response_json, self.ms_team_name )
        self.game.update( game_json )

    def find_game_by_team( self, i_game_day_json, i_team_name ):
        games = []
        for game in i_game_day_json['data']['games']['game']:
            if game['home_team_name'] == i_team_name or game['away_team_name'] == i_team_name:
                games.append( game )
                if game['status']['status'] == "In Progress":
                    return game
        return games[-1]

    def request_gameday_data( self ):
        scoreboard_day_utc = time_utils.get_datetime_from_utc()
        year = scoreboard_day_utc.year
        month = scoreboard_day_utc.month
        day = scoreboard_day_utc.day

        url = 'http://gd2.mlb.com/components/game/mlb/year_%04i/month_%02i/day_%02i/master_scoreboard.json' % (year, month, day)

        resp      = requests.get( url )
        resp_json = json.loads( resp.content )
        return resp_json

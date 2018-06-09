import logger as paul_bunyan

DEFAULT_ARGS = {
    'debug': False,
    'virtual': True,
    'team': 'Red Sox',
    }

class Scoreboard:
    def __init__( self ):
        print 'init Scoreboard'
        self.mb_running = False

    def run( self, args = DEFAULT_ARGS ):
        self.mb_running = True
        while self.mb_running:
            if args['debug']:
                self.run_()
            else:
                try:
                    self.run_()
                except Exception as ex:
                    paul_bunyan.log_exception( ex )

    def run_( self ):
        print "Running Scoreboard"
        time.sleep( 5 )
        self.mb_running = False

    def find_game_by_team( i_game_day_json, i_team_name ):
        games = []
        for game in i_game_day_json['data']['games']['game']:
            if game['home_team_name'] == i_team_name or game['away_team_name'] == i_team_name:
                games.append( game )
                if game['status']['status'] == "In Progress":
                    return game
        return games[-1]

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
        self.mb_running = False

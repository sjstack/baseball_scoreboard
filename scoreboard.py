
class Scoreboard:
    def __init__( self ):
        print 'init Scoreboard'
        self.mb_running = False
        
    def run( self ):
        self.mb_running = True
        
        while self.mb_running:
            self.run_()

    def run_( self ):
        print "Running Scoreboard"
        self.mb_running = False

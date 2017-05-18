from scoreboard import *

class VirtualScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )
        print 'init VirtualScoreboard'
        
    def run_( self ):
        print "Running Virtual Scoreboard"
        self.mb_running = False

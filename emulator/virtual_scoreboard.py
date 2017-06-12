from scoreboard import *

class VirtualScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )

    def run_( self ):
        Scoreboard.run_( self )
        self.mb_running = False

from scoreboard import *

class PhysicalScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )
        import RPi.GPIO as gpio

    def run_( self ):
        Scoreboard.run_( self )
        self.mb_running = False

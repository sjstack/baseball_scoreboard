from scoreboard import *

class PhysicalScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )

        import RPi.GPIO as gpio

        print 'init PhysicalScoreboard'
        
    def run_( self ):
        print "Running Physical Scoreboard"
        self.mb_running = False

from scoreboard import *

class VirtualScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )

        # Init markers
        self.markers = { 'on_base': [ '', '', '' ],
                         'at_bat': { 'strikes': [ '', '', '' ],
                                     'balls': [ '', '', '' ] },
                         'hit': '' }

    def run_( self ):
        Scoreboard.run_( self )
        self.print_scoreboard()

    def print_scoreboard( self ):
        self.update_on_base_markers()
        self.update_error_marker()
        self.update_at_bat_markers()
        self.update_boxscore_markers()

        self.draw_scoreboard()

    def update_on_base_markers( self ):
        # Set on base markers
        self.on_base_markers = [" "] * 3
        for base_i in range( 3 ):
            self.markers['on_base'][base_i] = "X" if self.game_data.on_base[base_i] else " "

    def update_error_marker( self ):
        # Set error marker
        if self.game_data.error:
            self.markers['error'] = "X {0}".format( self.game_data.error )
        else:
            self.markers['error'] = "     "

    def update_at_bat_markers( self ):
        # Set strikes markers
        self.markers['at_bat']['strikes'] = \
            ["X"] * self.game_data.strikes + [" "] * (3 - self.game_data.strikes)

        # Set balls markers
        self.markers['at_bat']['balls'] = \
            ["X"] * self.game_data.balls + [" "] * (4 - self.game_data.balls)

        # Set Hit marker
        self.markers['hit'] = "X" if self.game_data.hit else " "

    def update_boxscore_markers( self ):
        print "Here"
        
    def draw_scoreboard( self ):
        print "There"

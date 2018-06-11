from scoreboard import *

class VirtualScoreboard( Scoreboard ):
    def __init__( self ):
        Scoreboard.__init__( self )

    def run_( self ):
        Scoreboard.run_( self )
        os.system( 'clear' )
        #self.print_game()
        self.mb_running = False

    def print_game( self ):
        error_map = { "error by pitcher": "E1",
                      "error by catcher": "E2",
                      "error by first baseman": "E3",
                      "error by second baseman": "E4",
                      "error by third baseman": "E5",
                      "error by shortstop": "E6",
                      "error by left fielder": "E7",
                      "error by center fielder": "E8",
                      "error by right fielder": "E9" }

        on_first = self.m_game["inning"]["bases"]["first"] != None
        first_marker = "X" if on_first else " "
        on_second = self.m_game["inning"]["bases"]["second"] != None
        second_marker = "X" if on_second else " "
        on_third = self.m_game["inning"]["bases"]["third"] != None
        third_marker = "X" if on_third else " "

        inning_str = str( self.m_game["inning"]["number"] ).rjust( 3, " " ).ljust( 5, " " )
        if self.m_game['inning']['status'] == "Final":
            inning_str = "Final"
        elif self.m_game['inning']['status'] == "Warmup":
            inning_str = "Warm'"
        elif self.m_game['inning']['status'] == "Pre-Game":
            inning_str = " Pre "
        top_inning_marker = " "
        bottom_inning_marker = " "

        if self.m_game["inning"]["state"] == "Top" or self.m_game["inning"]["state"] == "Middle":
            top_inning_marker = "-"
        if self.m_game["inning"]["state"] == "Bottom" or self.m_game["inning"]["state"] == "Middle":
            bottom_inning_marker = "-"

        at_bat_str = "  " if self.m_game["at_bat"]["batter"] == None else str( self.m_game["at_bat"]["batter"]["number"] ).rjust( 2, " " )
        pitcher_str = "  " if self.m_game["at_bat"]["pitcher"] == None else str( self.m_game["at_bat"]["pitcher"]["number"] ).rjust( 2, " " )

        one_strike = self.m_game["at_bat"]["count"]["strikes"] >= 1
        one_strike_marker = "X" if one_strike else " "

        two_strike = self.m_game["at_bat"]["count"]["strikes"] >= 2
        two_strike_marker = "X" if two_strike else " "

        three_strike = self.m_game["at_bat"]["count"]["strikes"] >= 3
        three_strike_marker = "X" if three_strike else " "

        one_ball = self.m_game["at_bat"]["count"]["balls"] >= 1
        one_ball_marker = "X" if one_ball else " "

        two_ball = self.m_game["at_bat"]["count"]["balls"] >= 2
        two_ball_marker = "X" if two_ball else " "

        three_ball = self.m_game["at_bat"]["count"]["balls"] >= 3
        three_ball_marker = "X" if three_ball else " "

        four_ball = self.m_game["at_bat"]["count"]["balls"] >= 4
        four_ball_marker = "X" if four_ball else " "

        hit_marker = "X" if hit else " "
        error_marker = "     "
        for error_key in error_map.keys():
            if self.m_game["last_play"] != None and self.m_game["last_play"].find( error_key ) != -1:
                error_marker = "X  {0}".format( error_map[error_key])

        one_out = self.m_game["inning"]["outs"] >= 1
        one_out_marker = "X" if one_out else " "

        two_out = self.m_game["inning"]["outs"] >= 2
        two_out_marker = "X" if two_out else " "

        away_team_name = self.m_game["away"]["name"].ljust( 20, " " )
        home_team_name = self.m_game["home"]["name"].ljust( 20, " " )

        away_inning_runs_1 = "   " if self.m_game["away"]["box"][0] == None else str( self.m_game["away"]["box"][0] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_2 = "   " if self.m_game["away"]["box"][1] == None else str( self.m_game["away"]["box"][1] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_3 = "   " if self.m_game["away"]["box"][2] == None else str( self.m_game["away"]["box"][2] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_4 = "   " if self.m_game["away"]["box"][3] == None else str( self.m_game["away"]["box"][3] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_5 = "   " if self.m_game["away"]["box"][4] == None else str( self.m_game["away"]["box"][4] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_6 = "   " if self.m_game["away"]["box"][5] == None else str( self.m_game["away"]["box"][5] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_7 = "   " if self.m_game["away"]["box"][6] == None else str( self.m_game["away"]["box"][6] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_8 = "   " if self.m_game["away"]["box"][7] == None else str( self.m_game["away"]["box"][7] ).rjust( 2, " " ).ljust( 3, " " )
        away_inning_runs_9 = "   " if self.m_game["away"]["box"][8] == None else str( self.m_game["away"]["box"][8] ).rjust( 2, " " ).ljust( 3, " " )

        home_inning_runs_1 = "   " if self.m_game["home"]["box"][0] == None else str( self.m_game["home"]["box"][0] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_2 = "   " if self.m_game["home"]["box"][1] == None else str( self.m_game["home"]["box"][1] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_3 = "   " if self.m_game["home"]["box"][2] == None else str( self.m_game["home"]["box"][2] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_4 = "   " if self.m_game["home"]["box"][3] == None else str( self.m_game["home"]["box"][3] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_5 = "   " if self.m_game["home"]["box"][4] == None else str( self.m_game["home"]["box"][4] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_6 = "   " if self.m_game["home"]["box"][5] == None else str( self.m_game["home"]["box"][5] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_7 = "   " if self.m_game["home"]["box"][6] == None else str( self.m_game["home"]["box"][6] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_8 = "   " if self.m_game["home"]["box"][7] == None else str( self.m_game["home"]["box"][7] ).rjust( 2, " " ).ljust( 3, " " )
        home_inning_runs_9 = "   " if self.m_game["home"]["box"][8] == None else str( self.m_game["home"]["box"][8] ).rjust( 2, " " ).ljust( 3, " " )

        away_runs_total = str( self.m_game["away"]["runs"] ).rjust( 2, " " ).ljust( 3, " " )
        away_hits_total = str( self.m_game["away"]["hits"] ).rjust( 2, " " ).ljust( 3, " " )
        away_errors_total = str( self.m_game["away"]["errors"] ).rjust( 2, " " ).ljust( 3, " " )

        home_runs_total = str( self.m_game["home"]["runs"] ).rjust( 2, " " ).ljust( 3, " " )
        home_hits_total = str( self.m_game["home"]["hits"] ).rjust( 2, " " ).ljust( 3, " " )
        home_errors_total = str( self.m_game["home"]["errors"] ).rjust( 2, " " ).ljust( 3, " " )

        print "==========================================================================================================="
        print "|                                                                                                         |"
        print "|  --------------------------------------------------------------------------------  -------------------  |"
        print "|  | Team                   |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  |  R  |  H  |  E  |  |"
        print "|  |------------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|  |-----|-----|-----|  |"
        print "|  |                        |     |     |     |     |     |     |     |     |     |  |     |     |     |  |"
        print "|  |  {0}  | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} |  | {10} | {11} | {12} |  |".format( away_team_name,
                                                                                                                      away_inning_runs_1,
                                                                                                                      away_inning_runs_2,
                                                                                                                      away_inning_runs_3,
                                                                                                                      away_inning_runs_4,
                                                                                                                      away_inning_runs_5,
                                                                                                                      away_inning_runs_6,
                                                                                                                      away_inning_runs_7,
                                                                                                                      away_inning_runs_8,
                                                                                                                      away_inning_runs_9,
                                                                                                                      away_runs_total,
                                                                                                                      away_hits_total,
                                                                                                                      away_errors_total )
        print "|  |                        |     |     |     |     |     |     |     |     |     |  |     |     |     |  |"
        print "|  |------------------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|  |-----|-----|-----|  |"
        print "|  |                        |     |     |     |     |     |     |     |     |     |  |     |     |     |  |"
        print "|  |  {0}  | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} |  | {10} | {11} | {12} |  |".format( home_team_name,
                                                                                                                      home_inning_runs_1,
                                                                                                                      home_inning_runs_2,
                                                                                                                      home_inning_runs_3,
                                                                                                                      home_inning_runs_4,
                                                                                                                      home_inning_runs_5,
                                                                                                                      home_inning_runs_6,
                                                                                                                      home_inning_runs_7,
                                                                                                                      home_inning_runs_8,
                                                                                                                      home_inning_runs_9,
                                                                                                                      home_runs_total,
                                                                                                                      home_hits_total,
                                                                                                                      home_errors_total )
        print "|  |                        |     |     |     |     |     |     |     |     |     |  |     |     |     |  |"
        print "|  |------------------------------------------------------------------------------|  |-----------------|  |"
        print "|                                                                                    |  BASE  RUNNERS  |  |"
        print "|                                                                                    |                 |  |"
        print "|  |______________________________________________________________________________|  |       [{0}]       |  |".format( second_marker )
        print "|  |            |                        |           |       |         |          |  |     /     \     |  |"
        print "|  |   AT BAT   |  BALLS:  {0}  {1}  {2}  {3}    |  PITCHER  |  HIT  |  ERROR  |   OUTS   |  |    /   {4}   \    |  |".format( one_ball_marker,
                                                                                                                                              two_ball_marker,
                                                                                                                                              three_ball_marker,
                                                                                                                                              four_ball_marker,
                                                                                                                                              top_inning_marker )
        print "|  |            |                        |           |       |         |          |  |  [{0}] {1} [{2}]  |  |".format( third_marker,
                                                                                                                                      inning_str,
                                                                                                                                      first_marker )
        print "|  |- - - - - - |------------------------|- - - - - -|- - - -|- - - - -|- - - - - |  |    \   {0}   /    |  |".format( bottom_inning_marker )
        print "|  |            |                        |           |       |         |          |  |     \     /     |  |"
        print "|  |     {0}     |  STRIKES:  {1}  {2}  {3}     |     {4}    |   {5}   |  {6}  |   {7}  {8}   |  |       [ ]       |  |".format( at_bat_str,
                                                                                                                                            one_strike_marker,
                                                                                                                                            two_strike_marker,
                                                                                                                                            three_strike_marker,
                                                                                                                                            pitcher_str,
                                                                                                                                            hit_marker,
                                                                                                                                            error_marker,
                                                                                                                                            one_out_marker,
                                                                                                                                            two_out_marker )
        print "|  |            |                        |           |       |         |          |  |                 |  |"
        print "|  |------------------------------------------------------------------------------|  |-----------------|  |"
        print "|                                                                                                         |"
        print "==========================================================================================================="

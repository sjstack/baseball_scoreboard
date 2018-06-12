import sys

sys.path.append('./utils')
from game_recorder import GameRecorder

DEFAULT_PARAMS = {
    'record': False,
    'home_team': "home",
    'away_team': "away",
    }

class GameState:
    def __init__( self, i_game_params = DEFAULT_PARAMS ):
        self.mb_record_mode = i_game_params['record'] if i_game_params.has_key( 'record' ) else DEFAULT_PARAMS['record']
        if self.mb_record_mode:
            self.m_game_recorder = GameRecorder()

        self.mb_hit  = False
        self.mi_hits = 0

        self.mb_error  = False
        self.mi_errors = 0

        self.mb_strike  = False
        self.mi_strikes = 0

        self.mb_ball  = False
        self.mi_balls = 0

        self.mb_out  = False
        self.mi_outs = 0

        self.m_inning    = InningState()
        home_team = i_game_params['home_team'] if i_game_params.has_key( 'home_team' ) else DEFAULT_PARAMS['home_team']
        self.m_home_team = TeamState( home_team )
        away_team = i_game_params['away_team'] if i_game_params.has_key( 'away_team' ) else DEFAULT_PARAMS['away_team']
        self.m_away_team = TeamState( away_team )

    def update( self, i_game_json ):
        if self.mb_record_mode:
            self.m_game_recorder.update_record( i_game_json )

        self.set_hits( i_game_json['linescore']['h'] )
        self.set_errors( i_game_json['linescore']['e'] )
        self.set_balls( i_game_json['status'] )
        self.set_strikes( i_game_json['status'] )
        self.set_outs( i_game_json['status'] )

        self.m_inning.update( i_game_json )
        self.m_home_team.update( i_game_json )
        self.m_away_team.update( i_game_json )

    def set_hits( self, i_linescore_hits ):
        total_hits   = int( i_linescore_hits['home'] ) + int( i_linescore_hits['away'] )
        self.mb_hit  = self.mi_hits > total_hits
        self.mi_hits = total_hits

    def set_errors( self, i_linescore_errors ):
        total_errors   = int( i_linescore_errors['home'] ) + int( i_linescore_errors['away'] )
        self.mb_error  = self.mi_errors > total_errors
        self.mi_errors = total_errors

    def set_balls( self, i_game_status ):
        key = 'balls' if i_game_status.has_key( 'balls' ) else 'b'
        num_balls     = int( i_game_status[key] )
        self.mb_ball  = num_balls != 0 and self.mi_balls > num_balls
        self.mi_balls = num_balls

    def set_strikes( self, i_game_status ):
        key = 'strikes' if i_game_status.has_key( 'strikes' ) else 's'
        num_strikes     = int( i_game_status[key] )
        self.mb_strike  = num_strikes != 0 and self.mi_strikes != num_strikes
        self.mi_strikes = num_strikes

    def set_outs( self, i_game_status ):
        key = 'outs' if i_game_status.has_key( 'outs' ) else 'o'
        num_outs     = int( i_game_status[key] )
        self.mb_out  = num_outs != 0 and self.mi_outs > num_outs
        self.mi_outs = num_outs

class InningState:
    def __init__( self ):
        self.mi_number = 0
        self.ms_status = ""
        self.ms_state  = ""
        self.mi_outs   = 0
        self.md_count  = { "balls": 0, "strikes": 0 }   

        self.m_pitcher = None
        self.m_batter  = None
        self.m_bases   = [ None, None, None ]

        self.ms_play_by_play = None

    def update( self, i_game ):
        self.mi_number = int( i_game['status']['inning'] )
        self.ms_status = str( i_game['status']['status'] )
        self.ms_state  = str( i_game['status']['inning_state'] )
        outs_key = 'outs' if i_game['status'].has_key( 'outs' ) else 'o'
        self.mi_outs   = int( i_game['status'][outs_key] )

        if "pitcher" in i_game:
            self.m_pitcher = { "number": int( i_game["pitcher"]["number"] ),
                               "name": str(  i_game["pitcher"]["name_display_roster"] ) }
        else:
            self.m_pitcher = None

        if "batter" in i_game:
            self.m_batter = { "number": int( i_game["batter"]["number"] ),
                              "name": str(  i_game["batter"]["name_display_roster"] ) }
            self.md_count = { "balls": int( i_game['status']['b'] ),
                              "strikes": int( i_game['status']['s'] ) }
        else:
            self.m_batter = None
            self.md_count  = { "balls": 0, "strikes": 0 }

        if "runners_on_base" in i_game:
            if "runner_on_1b" in i_game["runners_on_base"]:
                self.m_bases[0] = { "name": str( i_game["runners_on_base"]["runner_on_1b"]["name_display_roster"] ),
                                    "number": int( i_game["runners_on_base"]["runner_on_1b"]["number"] ) }
            else:
                self.m_bases[0] = None

            if "runner_on_2b" in i_game["runners_on_base"]:
                self.m_bases[1] = { "name": str( i_game["runners_on_base"]["runner_on_2b"]["name_display_roster"] ),
                                    "number": int( i_game["runners_on_base"]["runner_on_2b"]["number"] ) }
            else:
                self.m_bases[1] = None

            if "runner_on_3b" in i_game["runners_on_base"]:
                self.m_bases[2] = { "name": str( i_game["runners_on_base"]["runner_on_3b"]["name_display_roster"] ),
                                    "number": int( i_game["runners_on_base"]["runner_on_3b"]["number"] ) }
            else:
                self.m_bases[2] = None

            if "pbp" in i_game:
                self.ms_play_by_play = str( i_game["pbp"] )

class TeamState:
    def __init__( self, i_home_or_away ):
        self.ms_home_or_away = i_home_or_away

        self.ms_name  = ""
        self.mi_runs  = 0
        self.mi_hits  = 0
        self.mi_errors = 0

        self.ma_box   = [None]*9

    def update( self, i_game ):
        self.ms_name   = i_game["{0}_team_name".format( self.ms_home_or_away )]
        self.mi_runs   = i_game['linescore']['r'][self.ms_home_or_away]
        self.mi_hits   = i_game['linescore']['h'][self.ms_home_or_away]
        self.mi_errors = i_game['linescore']['e'][self.ms_home_or_away]

        if str( i_game['status']['status'] ) == "In Progress" or str( i_game['status']['status'] ) == "Final":
            innings = i_game['linescore']['inning']
            num_innings = len( innings )
            innings_class = innings.__class__
            if innings_class == dict:
                if self.ms_home_or_away in  innings and innings[self.ms_home_or_away] != "":
                    self.ma_box[0] = int( innings[self.ms_home_or_away] )

            elif innings_class == list:
                for inning_i in range( num_innings ):
                    if self.ms_home_or_away in  innings[inning_i] and innings[inning_i][self.ms_home_or_away] != "":
                        self.ma_box[inning_i] = int( innings[inning_i][self.ms_home_or_away] )


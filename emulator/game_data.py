
ERROR_MAP = {
    "error by pitcher": "E1",
    "error by catcher": "E2",
    "error by first baseman": "E3",
    "error by second baseman": "E4",
    "error by third baseman": "E5",
    "error by shortstop": "E6",
    "error by left fielder": "E7",
    "error by center fielder": "E8",
    "error by right fielder": "E9"
}

class GameData:
    def __init__( self ):
        self.on_base = [False] * 3
        self.last_play = None
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.error = None
        self.hit = None

    def parse_error_from_last_play( self ):
        for error_key in ERROR_MAP.keys():
            if self.game_data.last_play != None and self.game_data.last_play.find( error_key ) != -1:
                return error_map[error_key]
        return None

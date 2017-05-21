#!/usr/bin/python

import pprint as pp

import argparse
import requests
import json
import time
import sys
import os

from datetime import datetime, timedelta

def find_game_by_team( i_game_day_json, i_team_name ):
    games = []
    for game in i_game_day_json['data']['games']['game']:
        if game['home_team_name'] == i_team_name or game['away_team_name'] == i_team_name:
            games.append( game )
            if game['status']['status'] == "In Progress":
                return game
    return games[-1]

def get_datetime_from_utc( utc_datetime = datetime.utcnow(), hours_rewind=12 ):
    return utc_datetime - timedelta( hours=hours_rewind )

def print_game( game, hit, error ):
    error_map = { "error by pitcher": "E1",
                  "error by catcher": "E2",
                  "error by first baseman": "E3",
                  "error by second baseman": "E4",
                  "error by third baseman": "E5",
                  "error by shortstop": "E6",
                  "error by left fielder": "E7",
                  "error by center fielder": "E8",
                  "error by right fielder": "E9" }

    on_first = game["inning"]["bases"]["first"] != None
    first_marker = "X" if on_first else " "
    on_second = game["inning"]["bases"]["second"] != None
    second_marker = "X" if on_second else " "
    on_third = game["inning"]["bases"]["third"] != None
    third_marker = "X" if on_third else " "

    inning_str = str( game["inning"]["number"] ).rjust( 3, " " ).ljust( 5, " " )
    if game['inning']['status'] == "Final":
        inning_str = "Final"
    elif game['inning']['status'] == "Warmup":
        inning_str = "Warm'"
    elif game['inning']['status'] == "Pre-Game":
        inning_str = " Pre "
    top_inning_marker = " "
    bottom_inning_marker = " "

    if game["inning"]["state"] == "Top" or game["inning"]["state"] == "Middle":    
        top_inning_marker = "-"
    if game["inning"]["state"] == "Bottom" or game["inning"]["state"] == "Middle":
        bottom_inning_marker = "-"

    at_bat_str = "  " if game["at_bat"]["batter"] == None else str( game["at_bat"]["batter"]["number"] ).rjust( 2, " " )
    pitcher_str = "  " if game["at_bat"]["pitcher"] == None else str( game["at_bat"]["pitcher"]["number"] ).rjust( 2, " " )

    one_strike = game["at_bat"]["count"]["strikes"] >= 1
    one_strike_marker = "X" if one_strike else " "

    two_strike = game["at_bat"]["count"]["strikes"] >= 2
    two_strike_marker = "X" if two_strike else " "

    three_strike = game["at_bat"]["count"]["strikes"] >= 3
    three_strike_marker = "X" if three_strike else " "

    one_ball = game["at_bat"]["count"]["balls"] >= 1
    one_ball_marker = "X" if one_ball else " "

    two_ball = game["at_bat"]["count"]["balls"] >= 2
    two_ball_marker = "X" if two_ball else " "

    three_ball = game["at_bat"]["count"]["balls"] >= 3
    three_ball_marker = "X" if three_ball else " "

    four_ball = game["at_bat"]["count"]["balls"] >= 4
    four_ball_marker = "X" if four_ball else " "

    hit_marker = "X" if hit else " "
    error_marker = "     "
    for error_key in error_map.keys():
        if game["last_play"] != None and game["last_play"].find( error_key ) != -1:
            error_marker = "X  {0}".format( error_map[error_key])

    one_out = game["inning"]["outs"] >= 1
    one_out_marker = "X" if one_out else " "

    two_out = game["inning"]["outs"] >= 2
    two_out_marker = "X" if two_out else " "

    away_team_name = game["away"]["name"].ljust( 20, " " )
    home_team_name = game["home"]["name"].ljust( 20, " " )

    away_inning_runs_1 = "   " if game["away"]["box"][0] == None else str( game["away"]["box"][0] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_2 = "   " if game["away"]["box"][1] == None else str( game["away"]["box"][1] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_3 = "   " if game["away"]["box"][2] == None else str( game["away"]["box"][2] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_4 = "   " if game["away"]["box"][3] == None else str( game["away"]["box"][3] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_5 = "   " if game["away"]["box"][4] == None else str( game["away"]["box"][4] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_6 = "   " if game["away"]["box"][5] == None else str( game["away"]["box"][5] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_7 = "   " if game["away"]["box"][6] == None else str( game["away"]["box"][6] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_8 = "   " if game["away"]["box"][7] == None else str( game["away"]["box"][7] ).rjust( 2, " " ).ljust( 3, " " )
    away_inning_runs_9 = "   " if game["away"]["box"][8] == None else str( game["away"]["box"][8] ).rjust( 2, " " ).ljust( 3, " " )

    home_inning_runs_1 = "   " if game["home"]["box"][0] == None else str( game["home"]["box"][0] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_2 = "   " if game["home"]["box"][1] == None else str( game["home"]["box"][1] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_3 = "   " if game["home"]["box"][2] == None else str( game["home"]["box"][2] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_4 = "   " if game["home"]["box"][3] == None else str( game["home"]["box"][3] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_5 = "   " if game["home"]["box"][4] == None else str( game["home"]["box"][4] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_6 = "   " if game["home"]["box"][5] == None else str( game["home"]["box"][5] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_7 = "   " if game["home"]["box"][6] == None else str( game["home"]["box"][6] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_8 = "   " if game["home"]["box"][7] == None else str( game["home"]["box"][7] ).rjust( 2, " " ).ljust( 3, " " )
    home_inning_runs_9 = "   " if game["home"]["box"][8] == None else str( game["home"]["box"][8] ).rjust( 2, " " ).ljust( 3, " " )

    away_runs_total = str( game["away"]["runs"] ).rjust( 2, " " ).ljust( 3, " " )
    away_hits_total = str( game["away"]["hits"] ).rjust( 2, " " ).ljust( 3, " " )
    away_errors_total = str( game["away"]["errors"] ).rjust( 2, " " ).ljust( 3, " " )

    home_runs_total = str( game["home"]["runs"] ).rjust( 2, " " ).ljust( 3, " " )
    home_hits_total = str( game["home"]["hits"] ).rjust( 2, " " ).ljust( 3, " " )
    home_errors_total = str( game["home"]["errors"] ).rjust( 2, " " ).ljust( 3, " " )

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description = '' )
    parser.add_argument('--team', action='store', default="Red Sox", type=str, help='')
    parser.add_argument("-v", "--virtual", help="Run scoreboard in virtual mode.", action="store_true")
    args = parser.parse_args()

    scoreboard_day_utc = get_datetime_from_utc()    
    year = scoreboard_day_utc.year
    month = scoreboard_day_utc.month
    day = scoreboard_day_utc.day

    url = 'http://gd2.mlb.com/components/game/mlb/year_%04i/month_%02i/day_%02i/master_scoreboard.json' % (year, month, day)

    hits = 0
    errors = 0
    strikes = 0
    balls = 0
    outs = 0

    if not args.virtual:
        import RPi.GPIO as gpio
        gpio.setmode( gpio.BOARD )
        pins = [ 3, 5, 7, 31, 33, 35, 37, 36, 38, 40 ]
        gpio.setup(pins, gpio.OUT)

    while True:
        resp      = requests.get( url )
        resp_json = json.loads( resp.content )

        mlb_game = find_game_by_team( resp_json, args.team )

        if str(mlb_game['status']['status']) != "Preview":
            num_innings = len( mlb_game['linescore']['inning'] )
            mlb_linescore = mlb_game['linescore']
            mlb_innings   = mlb_linescore['inning']

            hit = hits != ( int( mlb_linescore['h']['home'] ) + int( mlb_linescore['h']['away'] ) )
            hits = ( int( mlb_linescore['h']['home'] ) + int( mlb_linescore['h']['away'] ) )

            error = errors != ( int( mlb_linescore['e']['home'] ) + int( mlb_linescore['e']['away'] ) )
            errors = ( int( mlb_linescore['e']['home'] ) + int( mlb_linescore['e']['away'] ) )

            ball = int( mlb_game['status']['b'] ) != 0 and balls != int( mlb_game['status']['b'] )
            balls = int( mlb_game['status']['b'] )

            strike = int( mlb_game['status']['s'] ) != 0 and strikes != int( mlb_game['status']['s'] )
            strikes = int( mlb_game['status']['s'] )

            out = int( mlb_game['status']['o'] ) != 0 and outs != int( mlb_game['status']['o'] )
            outs = int( mlb_game['status']['o'] )

            if outs >= 1:
                gpio.output( 7, gpio.HIGH )
            else:
                gpio.output( 7, gpio.LOW )

            if outs >= 2:
                gpio.output( 5, gpio.HIGH )
            else:
                gpio.output( 5, gpio.LOW )

            if outs >= 3:
                gpio.output( 3, gpio.HIGH )
            else:
                gpio.output( 3, gpio.LOW )

            game = { "inning": { "number":  int( mlb_game['status']['inning'] ),
                                 "status": str( mlb_game['status']['status'] ),
                                 "state": str( mlb_game['status']['inning_state'] ),
                                 "outs": int( mlb_game['status']['o'] ),
                                 "bases": { "first": None,
                                            "second": None,
                                            "third": None } },
                     "home": { "name": str( mlb_game['home_team_name'] ),
                               "box": [None]*9,
                               "runs": int( mlb_linescore['r']['home'] ),
                               "hits": int( mlb_linescore['h']['home'] ),
                               "errors": int( mlb_linescore['e']['home'] ) },
                     "away": { "name": str( mlb_game['away_team_name'] ),
                               "box": [None]*9,
                               "runs": int( mlb_linescore['r']['away'] ),
                               "hits": int( mlb_linescore['h']['away'] ),
                               "errors": int( mlb_linescore['e']['away'] ) },
                     "at_bat": { "batter": None,
                                 "count": { "balls": 0,
                                            "strikes": 0 },
                                 "pitcher": None },
                     "last_play": None }

            if "pbp" in mlb_game:
                game["last_play"] = str( mlb_game["pbp"] )

            if "batter" in mlb_game:
                game["at_bat"]["batter"] = { "number": int( mlb_game["batter"]["number"] ),
                                             "name": str(  mlb_game["batter"]["name_display_roster"] ) }
                game["at_bat"]["count"] = { "balls": int( mlb_game['status']['b'] ),
                                            "strikes": int( mlb_game['status']['s'] ) }
                if not args.virtual:
                    if game["at_bat"]["count"]["strikes"] >= 1:
                        gpio.output(40, gpio.HIGH)
                    else:
                        gpio.output(40, gpio.LOW)

                    if game["at_bat"]["count"]["strikes"] >= 2:
                        gpio.output(38, gpio.HIGH)
                    else:
                        gpio.output(38, gpio.LOW)

                    if game["at_bat"]["count"]["strikes"] >= 3:
                        gpio.output(36, gpio.HIGH)
                    else:
                        gpio.output(36, gpio.LOW)

                    if game["at_bat"]["count"]["balls"] >= 1:
                        gpio.output(31, gpio.HIGH)
                    else:
                        gpio.output(31, gpio.LOW)

                    if game["at_bat"]["count"]["balls"] >= 2:
                        gpio.output(33, gpio.HIGH)
                    else:
                        gpio.output(33, gpio.LOW)

                    if game["at_bat"]["count"]["balls"] >= 3:
                        gpio.output(35, gpio.HIGH)
                    else:
                        gpio.output(35, gpio.LOW)

                    if game["at_bat"]["count"]["balls"] >= 4:
                        gpio.output(37, gpio.HIGH)
                    else:
                        gpio.output(37, gpio.LOW)
                        
            else:
                game["at_bat"]["batter"] = None

                gpio.output(40, gpio.LOW)
                gpio.output(38, gpio.LOW)
                gpio.output(36, gpio.LOW)
                gpio.output(31, gpio.LOW)
                gpio.output(33, gpio.LOW)
                gpio.output(35, gpio.LOW)
                gpio.output(37, gpio.LOW)

            if "pitcher" in mlb_game:
                game["at_bat"]["pitcher"] = { "number": int( mlb_game["pitcher"]["number"] ),
                                              "name": str(  mlb_game["pitcher"]["name_display_roster"] ) }
            else:
                game["at_bat"]["pitcher"] = None

            if "runners_on_base" in mlb_game:
                if "runner_on_1b" in mlb_game["runners_on_base"]:
                    game["inning"]["bases"]["first"] = { "name": str( mlb_game["runners_on_base"]["runner_on_1b"]["name_display_roster"] ),
                                                         "number": int( mlb_game["runners_on_base"]["runner_on_1b"]["number"] ) }
                else:
                    game["inning"]["bases"]["first"] = None

                if "runner_on_2b" in mlb_game["runners_on_base"]:
                    game["inning"]["bases"]["second"] = { "name": str( mlb_game["runners_on_base"]["runner_on_2b"]["name_display_roster"] ),
                                                          "number": int( mlb_game["runners_on_base"]["runner_on_2b"]["number"] ) }
                else:
                    game["inning"]["bases"]["second"] = None

                if "runner_on_3b" in mlb_game["runners_on_base"]:
                    game["inning"]["bases"]["third"] = { "name": str( mlb_game["runners_on_base"]["runner_on_3b"]["name_display_roster"] ),
                                                         "number": int( mlb_game["runners_on_base"]["runner_on_3b"]["number"] ) }
                else:
                    game["inning"]["bases"]["third"] = None

            if str( mlb_game['status']['status'] ) == "In Progress" or str( mlb_game['status']['status'] ) == "Final":
                innings_class = mlb_innings.__class__
                if innings_class == dict:
                    if 'home' in mlb_innings and mlb_innings['home'] != "":
                        game["home"]["box"][0] = int( mlb_innings['home'] )

                    if 'away' in mlb_innings and mlb_innings['away'] != "":
                        game["away"]["box"][0] = int( mlb_innings['away'] )
                elif innings_class == list:
                    for inning_i in range( num_innings ):
                        if 'home' in mlb_innings[inning_i] and mlb_innings[inning_i]['home'] != "":
                            game["home"]["box"][inning_i] = int( mlb_innings[inning_i]['home'] )

                        if 'away' in mlb_innings[inning_i] and mlb_innings[inning_i]['away'] != "":
                            game["away"]["box"][inning_i] = int( mlb_innings[inning_i]['away'] )

            os.system( 'clear' )
            print_game( game, hit, error )
            time.sleep( 5 )

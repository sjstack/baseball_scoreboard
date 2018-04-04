#!/usr/bin/python

import sys

sys.path.append('./utils')
import time_utils

if __name__ == "__main__":
    scoreboard_day_utc = get_datetime_from_utc()
    year = scoreboard_day_utc.year
    month = scoreboard_day_utc.month
    day = scoreboard_day_utc.day

    url = 'http://gd2.mlb.com/components/game/mlb/year_%04i/month_%02i/day_%02i/master_scoreboard.json' % (year, month, day)

    last_resp_json = None
    last_resp_time = None
    while True:
        resp      = requests.get( url )
        resp_time = get_datetime_from_utc()
        resp_json = json.loads( resp.content )

        if resp_json != last_resp_json or last_resp_json == None:
            # save resp_json with time diff
            
            last_resp_json = resp_json
            last_resp_time = resp_time

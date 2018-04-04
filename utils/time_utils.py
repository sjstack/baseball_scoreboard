from datetime import datetime, timedelta

def get_datetime_from_utc( utc_datetime = datetime.utcnow(), hours_rewind=12 ):
    return utc_datetime - timedelta( hours=hours_rewind )

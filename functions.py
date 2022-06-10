import time
from datetime import datetime

def current_time_millis():
    return round(time.time() * 1000)

def formatedDate(millis):
    ms = int(millis)
    # return datetime.utcfromtimestamp(ms//1000).replace(microsecond=ms%1000*1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return datetime.utcfromtimestamp(ms//1000).strftime('%m-%d %I:%M%p')
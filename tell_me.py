from datetime import datetime
import time
import mysql_op


def tell_process(info):
    timestamp = int(time.time())
    res = "INSERT INTO `tell_me` (time_, message) VALUES (%s, '%s')" % (
        timestamp, info)
    mysql_op.execute(res)
    res = "INSERT INTO `tell_me_back_up` (time_, message) VALUES (%s, '%s')" % (
        timestamp, info)
    mysql_op.execute(res)
    return True

def tell_event():
    res = 'select * from `tell_me` order by time_ asc'
    info = mysql_op.sel(res)
    try:
        time_ = info[0]
    except:
        return False
    mon_, day_ = time.localtime(time_).tm_mon, time.localtime(time_).tm_mday
    hour_, minute_ = time.localtime(time_).tm_hour, time.localtime(time_).tm_min
    time_ = [mon_, day_, hour_, minute_]
    mon, day = datetime.today().month, datetime.today().day
    hour, minute, sec = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    time_now = [mon, day, hour, minute]
    if time_ == time_now:
        res = 'delete from `tell_me` order by time asc limit 1'
        mysql_op.execute(res)
        return info[1]
    else:
        return False

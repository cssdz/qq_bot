from datetime import datetime
import time
import mysql_op

year = 2023


def re_process(info, group_id, user_id):
    try:
        mon, day, hour, minute = info[7:9], info[10:12], info[13:15], info[16:18]
    except ValueError:
        return "格式错误！"
    dt = datetime.strptime("%s.%s.%s.%s.%s.00" % (year, mon, day, hour, minute), "%Y.%m.%d.%H.%M.%S")
    timestamp = int(time.mktime(dt.timetuple()))
    timestamp_now = int(time.time())
    if timestamp < timestamp_now:
        return "Time Error!"
    event = info[19:]

    res = "INSERT INTO `remind` (time, group_id, user_id, event) VALUES (%s, %s, %s, '%s')" % (
        timestamp, group_id, user_id, event)
    mysql_op.execute(res)
    res = "INSERT INTO `remind_backup` (time, group_id, user_id, event) VALUES (%s, %s, %s, '%s')" % (
        timestamp, group_id, user_id, event)
    mysql_op.execute(res)
    return "Get it!!"

def remind_event():
    res = 'select * from `remind` order by time asc'
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
        res = 'delete from `remind` order by time asc limit 1'
        mysql_op.execute(res)
        return info[1], info[2], info[3]
    else:
        return False

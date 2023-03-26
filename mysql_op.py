import pymysql

db = pymysql.connect(host='localhost', user='root', password='zixingche', database='qq_bot')


def city_code(city):
    res = "SELECT `adcode` FROM `city_code` WHERE `中文名` = '%s'" % city
    return sel(res)[0]


def save_message(time, group_id, user_id, raw_message):
    res = "INSERT INTO `message` (`time`, `group_id`, `user_id`, `raw_message`) VALUES (%s, %s, %s, '%s')" % (
        time, group_id, user_id, raw_message)
    print(res)
    execute(res)


def sel(res):
    try:
        cursor = db.cursor()
        cursor.execute(res)
        code = cursor.fetchone()
        return code
    except:
        print('error')
        db.rollback()


def execute(res):
    try:
        cursor = db.cursor()
        cursor.execute(res)
        db.commit()
    except:
        print('error')
        db.rollback()

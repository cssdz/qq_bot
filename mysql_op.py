import pymysql

db = pymysql.connect(host='localhost', user='root', password='zixingche', database='qq_bot')


def city_code(city):
    cursor = db.cursor()
    res = "SELECT `adcode` FROM `city_code` WHERE `中文名` = '%s'" % city
    cursor.execute(res)
    code = cursor.fetchone()
    return code[0]


def save_message(time, group_id, user_id, raw_message):
    cursor = db.cursor()
    res = "INSERT INTO `message` (`time`, `group_id`, `user_id`, `raw_message`) VALUES (%s, %s, %s, '%s')" % (
        time, group_id, user_id, raw_message)
    print(res)
    try:
        # 执行sql语句
        cursor.execute(res)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print('error')
        db.rollback()

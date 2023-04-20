import datetime
import json
import time
import weather
from sanic import Sanic
import trpg
import mysql_op
import TaskBoard
import remind
import translate
import tell_me
import KFC_remind
import random_attribute

app = Sanic('qqbot')
at = '[CQ:at,qq=1154850482]'
reply_list = ['在？', '在不？', '在吗？', '滴滴', '？', '1']
switch = False


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        # print(request)
        data = await ws.recv()
        data = json.loads(data)
        # print(data)
        # if 判断是群消息且文本消息不为空
        if data.get('message_type') == 'group' and data.get('raw_message'):
            raw_message = data['raw_message']
            raw_sender = data['sender']
            raw_nickname = raw_sender.get('nickname')
            raw_card = raw_sender.get('card')
            group_id = data['group_id']
            user_id = data['user_id']
            time_ = int(data['time'])

            # print(data)
            ret = group_message(raw_message, time_, raw_card, raw_nickname, group_id, user_id)
            await ws.send(json.dumps(ret))

        if data.get('message_type') == 'private' and data.get('raw_message'):
            raw_message = data['raw_message']
            raw_sender = data['sender']
            raw_nickname = raw_sender.get('nickname')
            user_id = data['user_id']
            time_ = int(data['time'])

            ret, mode = private_message(raw_message, time_, raw_nickname, user_id)
            await ws.send(json.dumps(ret))
            if mode == "trpg":
                text, group_id = "kp进行了暗骰！", 386781905
                ret = group_ret(group_id, text)
                await ws.send(json.dumps(ret))

        else:
            status = 0
            text, group_id, user_id = "", 701209234, 3271993008
            hour, minute, sec, weekday = time.localtime().tm_hour, time.localtime().tm_min, \
                time.localtime().tm_sec, datetime.datetime.now().weekday()
            info = remind.remind_event()
            info_1 = tell_me.tell_event()
            info_2 = KFC_remind.kfc(hour, minute, weekday)

            if info is not False:
                group_id, user_id, text = info

            if info_1 is not False:
                text, status = info_1, 1

            if info_2 is not None:
                text = info_2

            if hour == 6 and minute == 30 and sec in range(5):
                group_id = 771695831
                text = weather.weather(city_code=411300)
                text += "\n%s" % TaskBoard.board_message(7)
                time.sleep(5)

            if hour == 6 and minute == 30 and sec in range(30, 35):
                group_id = 771695831
                text += "%s" % TaskBoard.board_message(5)
                time.sleep(5)

            if text != "":
                ret = ""
                if status == 0:
                    ret = group_ret(group_id, text)
                if status == 1:
                    ret = group_ret(user_id, text)
                await ws.send(json.dumps(ret))


def private_ret(user_id, text):
    ret = {
        'action': 'send_private_msg',
        'params': {
            'user_id': user_id,
            'message': text,
        }
    }
    return ret


def group_ret(group_id, text):
    ret = {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': text,
        }
    }
    return ret


# 个人消息
def private_message(raw_message, time_, nickname, user_id):
    global switch
    mode, text = "normal", ""

    # 开启骰子功能
    if raw_message == "trpg on":
        switch = True
        text = "GET READY"

    # 关闭骰子功能
    if raw_message == "trpg off":
        switch = False
        text = "SYSTEM OVER"

    if switch is True and raw_message.find('d') > 0:
        text, sum_ = trpg.roll(nickname, raw_message)
        if text is not False:
            user_id = 3271993008
            mode = "trpg"
            ret = private_ret(user_id, text)
            return ret, mode

    if raw_message in reply_list:
        text = '【自动回复】本人现在不在，有事请留言，最好不要以表情包和图片的形式告知。'
    if user_id != user_id:
        text = '【滴滴】' + nickname + '(' + str(user_id) + ')：' + raw_message
        user_id = 3271993008
    ret = private_ret(user_id, text)
    return ret, mode


# 群消息
def group_message(raw_message, time_, raw_card, raw_nickname, group_id=771695831, user_id=None):
    text = ""
    # 群昵称替换QQ名
    if raw_card == "":
        raw_card = raw_nickname

    # 避免存储图片表情等信息
    if 'CQ' in raw_message:
        raw_message = raw_message.split('[CQ', 1)[0]
        if raw_message == "":
            return

    # 计时提醒功能
    if 'remind' in raw_message:
        text = remind.re_process(raw_message, group_id, user_id)

    # 存储群消息
    mysql_op.save_message(time_, group_id, user_id, raw_message)

    # 询问天气
    if "天气" in raw_message:
        city_code = 411302
        raw_message = raw_message.strip("天气")
        if raw_message != "":
            city_code = mysql_op.city_code(raw_message)
        text = weather.weather(city_code)

    # 翻译功能
    if "fy " in raw_message:
        info = raw_message[3:]
        text = translate.connect(info)

    # 创建角色属性
    if raw_message == "roll role":
        text = random_attribute.rand_attribute(raw_card)

    # 骰子功能体现
    if raw_message.find('d') > 0:
        try:
            text, sum_ = trpg.roll(raw_card, raw_message)
        except TypeError:
            pass
        if text is False:
            return

    # 看板功能
    if "project" in raw_message and group_id == 771695831:
        try:
            no = int(raw_message[7:])
            text = TaskBoard.board_message(no + 3)
        except ValueError:
            return

    # 将发送信息打包为json格式并发送
    if text != '':
        ret = group_ret(group_id, text)
        return ret
    else:
        return False


if __name__ == "__main__":
    app.run(debug=True, port=5700, auto_reload=True, workers=2)

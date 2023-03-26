import json
import time
import weather
from sanic import Sanic
import trpg
import mysql_op
import TaskBoard
import remind
import translate

app = Sanic('qqbot')
switch = False
at = '[CQ:at,qq=1154850482]'
reply_list = ['在？', '在不？', '在吗？', '滴滴', '？']


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        print(request)
        data = await ws.recv()
        data = json.loads(data)
        print(data)
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

            ret = private_message(raw_message, time_, raw_nickname, user_id)
            await ws.send(json.dumps(ret))


# 个人消息
def private_message(raw_message, time_, nickname, user_id):
    if raw_message in reply_list:
        text = '【自动回复】本人现在不在，有事请留言，最好不要以表情包和图片的形式告知。'
    else:
        text, user_id = '【滴滴】' + nickname + '：' + raw_message, 3271993008
    ret = {
        'action': 'send_private_msg',
        'params': {
            'user_id': user_id,
            'message': text,
        }
    }
    return ret


# 群消息
def group_message(raw_message, time_, raw_card, raw_nickname, group_id=771695831, user_id=None):
    text = ""
    global switch
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
        print(info)
        text = translate.connect(info)

    # 开启骰子功能
    if raw_message == "trpg on":
        switch = True
        text = "GET READY"

    # 关闭骰子功能
    if raw_message == "trpg off":
        switch = False
        text = "SYSTEM OVER"

    # 骰子功能体现
    if switch is True and raw_message.find('d') > 0:
        text = trpg.roll(raw_card, raw_message)
        if text is False:
            return

    if "project" in raw_message and group_id == 771695831:
        try:
            no = int(raw_message[7:])
            text = TaskBoard.board_message(no + 3)
        except ValueError:
            return

    else:
        hour, minute, sec = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
        info = remind.remind_event()
        if info is not None:
            group_id, user_id, text = info

        if hour == 6 and minute == 30 and sec in range(5):
            text = weather.weather(city_code=411300)
            text += "\n%s" % TaskBoard.board_message(7)
            time.sleep(5)

        if hour == 6 and minute == 30 and sec in range(30, 35):
            text += "%s" % TaskBoard.board_message(5)
            time.sleep(5)

    # 将发送信息打包为json格式并发送
    if text != '':
        ret = {
            'action': 'send_group_msg',
            'params': {
                'group_id': group_id,
                'message': text,
            }
        }
        return ret


if __name__ == "__main__":
    app.run(debug=True, port=5700, auto_reload=True, workers=2)

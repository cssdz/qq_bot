import json
import time
import weather
from sanic import Sanic
import trpg
import mysql_op
import TaskBoard

app = Sanic('qqbot')
switch = False
at = '[CQ:at,qq=1154850482]'


@app.websocket('/qqbot')
async def qqbot(request, ws):
    """QQ机器人"""
    while True:
        print(request)
        city_code = 411300
        global switch
        hour, minute, sec = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
        # print(sec)
        data = await ws.recv()
        data = json.loads(data)
        text, group_id = "", 771695831
        # if 判断是群消息且文本消息不为空
        if data.get('message_type') == 'group' and data.get('raw_message'):
            # print(data)
            raw_message = data['raw_message']
            raw_sender = data['sender']
            raw_nickname = raw_sender.get('nickname')
            raw_card = raw_sender.get('card')
            group_id = data['group_id']
            user_id = data['user_id']
            time_ = int(data['time'])

            if ('image' or 'reply') in raw_message:
                continue

            mysql_op.save_message(time_, group_id, user_id, raw_message)
            # 群昵称替换QQ名
            if raw_card == "":
                raw_card = raw_nickname

            # 询问天气
            if "天气" in raw_message:
                raw_message = raw_message.strip("天气")
                if raw_message != "":
                    city_code = mysql_op.city_code(raw_message)
                text = weather.weather(city_code)

            # 开启骰子功能
            if raw_message == "trpg on":
                switch = True
                text = "GET READY"

            # 关闭骰子功能
            if raw_message == "trpg off":
                switch = False
                text = "SYSTEM OVER"

            # 骰子功能体现
            if switch is True and raw_message.find('d') == 1:
                text = trpg.roll(raw_card, raw_message)
                if text is False:
                    continue

            if "project" in raw_message and group_id == 771695831:
                try:
                    no = int(raw_message[7:])
                    text = TaskBoard.board_message(no + 3)
                except ValueError:
                    continue

        else:
            if hour == 6 and minute == 30 and sec in range(5):
                text = weather.weather(city_code)
                text += "\n%s" % TaskBoard.board_message(4)
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
            await ws.send(json.dumps(ret))


if __name__ == "__main__":
    app.run(debug=True, port=5700, auto_reload=True, workers=2)

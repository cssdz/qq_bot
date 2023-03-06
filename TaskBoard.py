import requests
import json
import time


def board_message(no):
    url = "http://kb.tcpcat.com/jsonrpc.php"

    payload = {
        "jsonrpc": "2.0",
        "method": "getBoard",
        "id": 3,
        "params": [no]
    }
    headers = {
        "content-type": "application/json",
        "Authorization": "Basic c2R6OjJkNDU3MGQ0ZGEwMmNkNjJiYzE5NDk1MGM2NWNiNTZiNWQ1NzcwZTYzNmQyZWY0YjhiN2YwYmNkMzY4Yw=="
    }

    response = requests.request("POST", url, json=payload, headers=headers).text

    info = json.loads(response)
    # print(info)
    info = info['result'][0]['columns']
    message_1, message_2, message_3, message_4 = ['待办', '预备', '进行中', '完成']
    line = '\n-----------------------------\n'

    for column in info:
        # print(column)
        tasks = column['tasks']
        for task in tasks:
            # print(task)
            column_name = task['column_name']
            if column_name == '待办':
                message_1 += message_process(task)

            if column_name == '预备':
                message_2 += message_process(task)

            if column_name == '进行中':
                message_3 += message_process(task)

            if column_name == '完成':
                message_4 += message_process(task)
    message = message_1 + line + message_2 + line + message_3 + line + message_4
    return message


def message_process(task):
    message_ = ''
    if task['title'] is None:
        message_ += '\n暂无信息'
    message_ += '\n%s\n标签:' % task['title']
    for tag in task['tags']:
        # print(tag['name'])
        message_ += '%s ' % tag['name']
    date_1 = int(task['date_due'])
    date_2 = time.localtime(date_1)
    other_style_time = time.strftime("%Y-%m-%d", date_2)
    message_ += '\n截止日期：%s\n' % other_style_time
    return message_

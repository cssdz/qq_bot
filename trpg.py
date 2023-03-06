import random


def roll(raw_card, raw_message):
    text, z, judge = "", 0, True
    info = raw_message.split('d', 2)
    try:
        x, y = int(info[0]), int(info[1])
    except ValueError:
        return False
    if x != 1:
        judge = False
    while x:
        res = random.randint(1, y)
        if y == 100 and res > 95:
            text = "大失败！"
        if y == 100 and res == 1:
            text = "大成功！"
        text += str(res)
        if x != 1:
            text += "   "
        x -= 1
        z += res
    text = raw_card + "的投掷结果为：" + text
    if judge is False:
        text += "   总计：%s" % z
    return text

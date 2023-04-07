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
        i = x
        while i:
            res = random.randint(1, y)
            text += str(res)
            if x != 1:
                text += "   "
            i -= 1
            z += res

    else:
        res = random.randint(1, y)
        if y == 100 and res > 95:
            text = "%s, 大失败！" % res
        elif y == 100 and res == 1:
            text = "%s, 大成功！" % res
        else:
            text = "%s" %res
    text = raw_card + "的投掷结果为：" + text
    if judge is False:
        text += "   总计：%s" % z
    return text, z

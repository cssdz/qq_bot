import trpg


# COC第七版随机人物属性生成
def rand_attribute(raw_card):
    attribute = {"力量STR": 0, "体质CON": 0, "体型SIZ": 1, "敏捷DEX": 0, "外貌APP": 0, "智力INT": 1, "意志POW": 0,
                 "教育EDU": 1, "幸运LUCK": 0}
    others = {"理智SAN": 2, "生命值HP": 2, "魔法值MP": 2, "伤害奖励DB": 2, "体格": 2, "移动力MOV": 2}
    attribute_key = attribute.keys()
    sum_ = 0

    # 为基础人物属性按一定规则随机赋值
    for key in attribute_key:
        num = 0
        value = attribute[key]
        # print(value)
        if value == 0:
            raw_message = "3d6"
            text, num = trpg.roll(raw_card, raw_message)
            num *= 5
            attribute[key] = num

        if value == 1:
            raw_message = "2d6"
            text, num = trpg.roll(raw_card, raw_message)
            num = (num + 6) * 5
            attribute[key] = num

        if key != "幸运LUCK":
            sum_ += num

    # 根据一定规则为其余属性赋值
    others["理智SAN"] = attribute["意志POW"]
    others["生命值HP"] = int((attribute["体质CON"] + attribute["体型SIZ"]) / 10)
    others["魔法值MP"] = attribute["意志POW"] / 5
    str_siz = attribute["力量STR"] + attribute["体型SIZ"]
    others["伤害奖励DB"], others["体格"] = select_db(others, str_siz)
    others["移动力MOV"] = select_mov(others, attribute)

    # 以文本格式输出
    return print_text(raw_card, attribute, others, sum_)


# 伤害奖励和体格制定规则
def select_db(others, str_siz):
    if 2 <= str_siz <= 64:
        others["伤害奖励DB"], others["体格"] = -2, -2

    elif 65 <= str_siz <= 84:
        others["伤害奖励DB"], others["体格"] = -1, -1

    elif 85 <= str_siz <= 124:
        others["伤害奖励DB"], others["体格"] = 0, 0

    elif 125 <= str_siz <= 164:
        text, others["伤害奖励DB"] = trpg.roll("", "1d4")
        others["体格"] = 1

    else:
        text, others["伤害奖励DB"] = trpg.roll("", "1d6")
        others["体格"] = 2

    return others["伤害奖励DB"], others["体格"]


# 移动力制定规则
def select_mov(others, attribute):
    if attribute["敏捷DEX"] < attribute["体型SIZ"] & attribute["力量STR"] < attribute["体型SIZ"]:
        others["移动力MOV"] = 7

    elif attribute["敏捷DEX"] > attribute["体型SIZ"] & attribute["力量STR"] > attribute["体型SIZ"]:
        others["移动力MOV"] = 9

    else:
        others["移动力MOV"] = 8

    return others["移动力MOV"]


# 将属性用文本形式描述
def print_text(raw_card, attribute, others, sum_):
    text = "%s的调查员属性：\n" % raw_card
    att_keys = attribute.keys()
    oth_keys = others.keys()

    for att in att_keys:
        text += "%s=%s/%d/%d\n" % (att, attribute[att], int(attribute[att] / 2), attribute[att] / 5)
    text += "共计:%d\n" % sum_

    for oth in oth_keys:
        text += "%s=%s" % (oth, others[oth])
        if oth != "移动力MOV":
            text += "\n"

    return text

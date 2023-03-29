kfc_status = 0

def kfc(hour, minute, week):
    global kfc_status
    if week == 3 and hour == 8 and minute == 0 and kfc_status == 0:
        text = "今天是疯狂星期四，请全体群员vivo50，望周知"
        kfc_status = 1
        return text

    if minute == 1:
        kfc_status = 0
    return None

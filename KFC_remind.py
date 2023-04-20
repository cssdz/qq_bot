kfc_status = 0

def kfc(hour, minute, week):
    global kfc_status
    if week == 3 and hour == 18 and minute == 30 and kfc_status == 0:
        print("test")
        text = "今天是疯狂星期四，请全体群员vivo50，望周知❤"
        kfc_status = 1
        return text

    if minute == 1 and kfc_status == 1:
        kfc_status = 0
    return None

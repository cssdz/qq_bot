import requests
import re


def weather(city_code):
    week_info = ['一', '二', '三', '四', '五', '六', '日']
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?' \
          'key=eec4ab98194cf860766846434a63ac84&city=%s&extensions=all' % city_code
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}

    info = requests.get(url, headers=headers).text

    pattern = '.*?"city":"(.*?)".*?"date":"(.*?)","week":"(.*?)","dayweather":"(.*?)"' \
              ',"nightweather":"(.*?)","daytemp":"(.*?)","nighttemp":"(.*?)","daywind":"(.*?)","nightwind":"(.*?)"'
    results = re.findall(pattern, info, re.S)[0]
    city, date, week_num, status_1, status_2, max_, min_, wind_1, wind_2 = results

    if status_1 == status_2:
        text_1 = "天气%s" % status_1
    else:
        text_1 = "天气%s转%s" % (status_1, status_2)

    if wind_1 == wind_2:
        wind = "今天风向为%s风" % wind_1
    else:
        wind = "白天为%s风，晚上为%s风" % (wind_1, wind_2)

    sub = abs(int(max_) - int(min_))
    week = week_info[int(week_num) - 1]

    if sub > 10:
        add = "温差较大，注意保暖♥"
    else:
        add = "温差适中~"

    text = "今天是%s，星期%s，%s%s，温度%s到%s度，%s，%s" % (
        date, week, city, text_1, max_, min_, wind, add)
    return text


# text = info.get('forecasts')
# print(text)

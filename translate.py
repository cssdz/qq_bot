import sys
import uuid
import requests
import hashlib
from importlib import reload
import time
import json

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '4c3b0ac3db22e7c4'
APP_SECRET = 'zwTnobZVEHAFpbWytLnucm8eJjdHKCmY'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(info):
    q = info
    data = {}
    data['from'] = 'auto'
    data['to'] = 'auto'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    # data['vocabId'] = "您的用户词表ID"

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()

    else:
        info = json.loads(response.content)
        text = info['translation'][0] + '\n'
        try:
            explains = info['basic']['explains']
            for i in range(len(explains)):
                if i != len(explains) - 1:
                    text += explains[i] + '\n'
                else:
                    text += explains[i]
        except KeyError:
            return False
        return text
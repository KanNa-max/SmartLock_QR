import requests
import json
import datetime
import urllib.request

URL = 'http://127.0.0.1:3000'  # http接続先

# 日付データ取得(yyyymmddhhmmss) , 既定のフォーマットに成形
def get_now():
    dt_now = datetime.datetime.now()
    now = "%04d%02d%02d%02d%02d%02d" % (
        dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)
    return now

# "開閉記録のデータモデル"にデータを追加
def api_add(id = "none", is_open = "none", comment = "none"):
    data = {"dev_id": id,
           # "send_date": now,
            "is_open": is_open,
            "comment": comment}
    print(json.dumps(data))
    response = requests.post("%s/add" % URL, data=json.dumps(data))
    print(response)

# "鍵の開閉命令のデータモデル"にデータを追加
def api_addKey(key_ope="none"):
    data = {
        # "send_date": send_date, 
        "key_ope": key_ope}
    print(json.dumps(data))
    response = requests.post("%s/add_key" % URL, data=json.dumps(data))
    print(response)

# "鍵の開閉命令のデータモデル"から最新のデータを確認
def check_key():
    response = urllib.request.urlopen("%s/get_key" % URL)
    print("<Response [", response.getcode(), "]>")
    html = response.read()
    json_data = html.decode('utf-8')
    data = json.loads(json_data)
    print(json_data)
    # print("send_date: ",data['send_date'])
    # print("key_ope: ",data['key_ope'])
    return data['key_ope']


# api_add(id = "aaa", is_open = "True", comment = "test")
# api_addKey(key_ope = "open")
# check_key()
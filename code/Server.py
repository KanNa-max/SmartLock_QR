import os
from flask import Flask, render_template, jsonify, make_response, abort, request
import peewee
from peewee import fn
import json
import datetime

# 日付データ取得(yyyymmddhhmmss) , 既定のフォーマットに成形
dt_now = datetime.datetime.now()
now = "%04d%02d%02d%02d%02d%02d" % (
    dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)

# 初期設定
app = Flask(__name__)

# データベースを削除(test用)
if os.path.exists("./tmp/data.db"):
    os.remove("./tmp/data.db")

# SQLiteDBの生成
if not os.path.exists('./tmp'):
    os.mkdir('./tmp')
db = peewee.SqliteDatabase("./tmp/data.db")


################################################################################
## データモデルクラス ##

# 開閉データ
class DataModel(peewee.Model):
    dev_id = peewee.TextField()
    send_date = peewee.IntegerField()
    is_open = peewee.TextField()
    comment = peewee.TextField()

    class Meta:
        database = db

# 鍵の開閉命令
class KeyOperand(peewee.Model):
    send_date = peewee.IntegerField()
    key_ope = peewee.TextField()

    class Meta:
        database = db


################################################################################


# テーブルの作成
db.create_tables([DataModel, KeyOperand])

# server起動時の初回データ
DataModel.create(dev_id="server", send_date=now,
                 is_open="none", comment="default")
KeyOperand.create(send_date=now, key_ope="none")

### 登録API ###

# データ追加 "開閉記録のデータモデル"
@app.route('/add', methods=['POST'])
def addData():
    data = json.loads(request.data.decode('utf-8'))
    print(data)
    DataModel.create(dev_id=data["dev_id"],
                     send_date=now,
                     is_open=data["is_open"],
                     comment=data["comment"])
    return "{ok}"

# 最新データを取得 "開閉記録のデータモデル"
@app.route('/get', methods=['GET'])
def getData():
    max = DataModel.select(fn.MAX(DataModel.send_date)).scalar()
    data = DataModel.select().where(DataModel.send_date == max)
    for d in data:
        result = {"dev_id": d.dev_id,
                  "send_date": d.send_date,
                  "is_open": d.is_open,
                  "comment": d.comment}
    return make_response(jsonify(result))

# データ追加 "鍵の開閉命令のデータモデル"
@app.route('/add_key', methods=['POST'])
def addKey():
    data = json.loads(request.data.decode('utf-8'))
    print(data)
    KeyOperand.create(send_date=now, key_ope=data["key_ope"])
    return "{ok}"

# 最新データを取得 "鍵の開閉命令のデータモデル"
@app.route('/get_key', methods=['GET'])
def getKey():
    max = KeyOperand.select(fn.MAX(KeyOperand.send_date)).scalar()
    data = KeyOperand.select().where(KeyOperand.send_date == max)
    for d in data:
        result = {"send_date": d.send_date, "key_ope": d.key_ope}
    # KeyOperand.create(send_date=now, key_ope="none")
    return make_response(jsonify(result))


# データモデルを引き渡し、Webページの表示
@app.route('/')
def index():
    data = DataModel.select()
    return render_template("index.html", data=data)

## データモデルの中身確認用 ##
# print("全データ(DataModel)-----------------")
# for data in DataModel.select():
#    print(data.dev_id, data.send_date, data.is_open, data.comment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)


import datetime
import os
import pyqrcode as qr
import string
import secrets
import shutil

# グラフの保存場所の作成
if not os.path.exists('./image'):
    os.mkdir('./image')
# 日付データ取得(yyyymmddhhmmss) , 既定のフォーマットに成形
dt_now = datetime.datetime.now()
now = "%04d%02d%02d%02d%02d%02d" % (
    dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)
FILE_PNG = "./image/qrcode_%s.png" % (now)

# パスワード生成
def pass_gen(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # chars += "%&$#()""
    return ''.join(secrets.choice(chars) for x in range(size))


# QRコード作成
def create_qr():
    pass_size = 12
    qr_data = pass_gen(pass_size)
    code = qr.create(qr_data, error='L', version=3, mode='binary')
    code.png(FILE_PNG, scale=5, module_color=[
        0, 0, 0, 128], background=[255, 255, 255])
    with open("./image/qr.txt", 'a') as f:
        f.write(qr_data + "\n")
    print(qr_data)  ##
    return FILE_PNG # 生成したQRコードのパスを返す

# パスワード、QRコードを削除
def del_qr():
    if os.path.exists("./image"):
        shutil.rmtree('./image')
    if not os.path.exists('./image'):
        os.mkdir('./image')

# create_qr()
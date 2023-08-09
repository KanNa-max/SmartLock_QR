import pyqrcode
import os
import datetime
import qrcode

# グラフの保存場所の作成
if not os.path.exists('./image'):
    os.mkdir('./image')
# 日付データ取得(yyyymmddhhmmss) , 既定のフォーマットに成形
dt_now = datetime.datetime.now()
now = "%04d%02d%02d%02d%02d%02d" % (
    dt_now.year, dt_now.month, dt_now.day, dt_now.hour, dt_now.minute, dt_now.second)

FILE_PNG = "./image/qrcode_%s.png" % (now)
QR_DATA = "This_is_test_data"

# QRコード作成


def QR_gen_1():
    code = pyqrcode.create(QR_DATA, error='L', version=3, mode='binary')
    code.png(FILE_PNG, scale=5, module_color=[
        0, 0, 0, 128], background=[255, 255, 255])


def QR_gen_2(input_data):
    qr = qrcode.QRCode(
        version=5,  # バージョン
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 誤り訂正レベル
        box_size=2,  # セルのサイズ
        border=8  # 余白の幅
    )
    qr.add_data(input_data)
    qr.make()
    img = qr.make_image()
    img.save(FILE_PNG)

# QR_gen_2()

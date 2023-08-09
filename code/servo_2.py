import RPi.GPIO as GPIO
import time
from enum import Enum

import module.send_data as SenD
import module.camera as camera
import module.QR_read as QRread

## pin設定 ##
GPIO.setmode(GPIO.BCM)

servo_pin = 4  # 制御パルス出力: GPIO4
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)  # GPIO.PWM([pin], [Hz])
# SG90...PWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms(=2.5%〜12%)

OpenCLose_pin = 17  # 部屋側の開閉ボタン
GPIO.setup(OpenCLose_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

chime_pin = 22  # このプログラムの終了ボタン
GPIO.setup(chime_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

QR_pin = 27  # QRコード読み取り用Webカメラの開始ボタン
GPIO.setup(QR_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

## 開閉操作関連 ##
open_degree, init_degree = 180, 90  # 開閉調整用パラメータ
open_speed = 3
# 開閉操作記憶用フラグ


class OpenClose(Enum):
    open = 1
    close = 2


OpenClose_f = OpenClose.open


def ChangeDegree(degree):  # Degreeで角度指定
    dc = 2.5 + (12.0-2.5)/180*(degree+90)
    servo.ChangeDutyCycle(dc)


camera_num = 1  # QRコード読み取り用Webカメラの撮影回数


def KeyOpen():
    for degree in range(0, open_degree+1, open_speed):  # open
        ChangeDegree(90-degree)  # start位置: 0, left
        time.sleep(0.05)
        servo.ChangeDutyCycle(0.0)
    for degree in range(0, init_degree+1, open_speed):  # set init_position
        ChangeDegree(degree+(-90))  # start位置: -90, right
        time.sleep(0.05)
        servo.ChangeDutyCycle(0.0)
    return OpenClose.close


def KeyClose():
    for degree in range(0, open_degree+1, open_speed):  # close
        ChangeDegree(degree+(-90))  # start位置: -90, right
        time.sleep(0.05)
        servo.ChangeDutyCycle(0.0)
    for degree in range(0, init_degree+1, open_speed):  # set init_position
        ChangeDegree(90-(degree))  # start位置: 90, left
        time.sleep(0.05)
        servo.ChangeDutyCycle(0.0)
    return OpenClose.open


''' main 関数 '''


def main():
    servo.start(0.0)
    OpenClose_f = OpenClose.close  # 開閉操作の初期動作

    while True:

        # WebAPI側からの開閉操作
        key_ope = SenD.check_key()
        time.sleep(2)
        if((key_ope == "open") and (OpenClose_f == OpenClose.open)):
            print("open")
            OpenClose_f = KeyOpen()  # open
            SenD.api_add(id="by api", is_open="True", comment="open")
            SenD.api_addKey(key_ope="none")  # key操作命令を取り消し
        elif((key_ope == "close") and (OpenClose_f == OpenClose.close)):
            print("close")
            OpenClose_f = KeyClose()  # close
            SenD.api_add(id="by api", is_open="False", comment="close")
            SenD.api_addKey(key_ope="none")  # key操作命令を取り消し

        # 物理ボタン側からの操作
        if(GPIO.input(OpenCLose_pin) == False):
            if(OpenClose_f == OpenClose.open):
                print("open")
                OpenClose_f = KeyOpen()  # open
                SenD.api_add(id="by button", is_open="True", comment="open")
            elif(OpenClose_f == OpenClose.close):
                print("close")
                OpenClose_f = KeyClose()  # close
                SenD.api_add(id="by button", is_open="False", comment="close")
            time.sleep(0.3)

        # QRコードによる認証
        if(GPIO.input(QR_pin) == False):
            for i in range(camera_num): 
                camera.take_pic()
                readQR = QRread.Read_QR()
                if(readQR != 0):
                    if((QRread.auth_qr(readQR) == True) and (OpenClose_f == OpenClose.open)):
                        print("open")
                        OpenClose_f = KeyOpen()  # open
                        SenD.api_add(id="by QR", is_open="True", comment="open")
                        break
                    elif((QRread.auth_qr(readQR) == True) and (OpenClose_f == OpenClose.close)):
                        print("close")
                        OpenClose_f = KeyClose()  # close
                        SenD.api_add(id="by QR", is_open="False", comment="close")
                        break
                time.sleep(0.5)
            time.sleep(0.3)

        # 通常終了
        if(GPIO.input(chime_pin) == False):
            print("Fin")  # fin
            break

    servo.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    main()

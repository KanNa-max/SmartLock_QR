from pyzbar.pyzbar import decode
from PIL import Image

# QRコードを読み取れたら値を返す
def Read_QR():
    read_qr = decode(Image.open('./image/pic_test.jpg'))
    if(read_qr != []):
        ans = read_qr[0].data.decode("utf-8")
        print(ans)
        return ans
    else:
        print("false:qr read")
        return 0

## 認証したQRコードリストに入力データ

def auth_qr(input_str):
    with open("./image/qr.txt", "r") as f:
        qr_data = [s.strip() for s in f.readlines()]

    for data in qr_data:
        if(data == input_str):
            return True
    return False
        
'''
ans = Read_QR()
if(ans != 0):
    print(ans)
'''


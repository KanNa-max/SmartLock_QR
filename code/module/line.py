import requests

url = "https://notify-api.line.me/api/notify"
access_token = 'hogahoga_hugehuge' #  アクセストークン
headers = {'Authorization': 'Bearer ' + access_token}

def send_img(path, message):
    image = path
    payload = {'message': message}
    files = {'imageFile': open(image, 'rb')}
    requests.post(url, headers=headers, params=payload, files=files)

def send_msg(message):
    payload = {'message': message}
    requests.post(url, headers=headers, params=payload)


# PATH = '/home/hira/Documents/code/image/qrcode_20220201140249.png'
# send_img(PATH, '認証用QRコード')
# send_msg("test")
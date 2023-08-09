import module.line as line
import module.pas_gen2QR as pas_gen2QR

img_path = pas_gen2QR.create_qr()
line.send_img(img_path, "認証用QRコード")
# Raspberry Piでスマートロックをつくる
419024 平野悠人

## このフォルダについて
情報工学実験Ⅲの自由実験「Raspberry Piでスマートロックをつくる」で
作成した各種データが保存してある.

## ファイル構成
+ 3DCAD
    + servo_double v2.f3z\
        Fusion360で作成した3DCADのアーカイブデータ
    + servo_double v2.stl\
        Fusion360で作成した3DCADのstlデータ
+ arduino\
    m5stick用の鍵開閉操作コード
+ image\
QRコード関連の一時ファイル(パスワード保存用,Webカメラの撮影画像)
+ module\
作成した関数化したソースコード類
    + camera.py\
        Webカメラ撮影
    + line.py\
        LINE Notify
    + pas_gen.py\
        パスワード生成
    + pas_gen2QR.py\
        パスワード生成、QRコード生成を一括化
    + QR_gen.py\
        QRコード生成
    + QR_read.py\
        QRコードの読み取り、認証
    + RSA.py\
        RSAの公開鍵暗号方式で暗号化
    + send_data.py\
        Serverに対する操作を関数化
+ slackbot\
    slack上で鍵の開閉操作を行える(未完成)
+ templates\
    開閉データのログ "DataModel" 確認用の簡易的なWebページ
+ tmp\
    データベースの保存フォルダ
+ README.md\
    このファイル
+ sample.py\
    鍵の開閉命令 "KeyOperand"へのデータ追加を間接的に実行
+ send_QR.py\
    パスワード生成、QRコード生成、LINE NotifyでのQRコードの配布を一括化
+ Server.py\
    Server起動用
+ servo_1.py\
    WebAPIを実装後のメインコード
+ servo_2.py\
    QRコード認証システム採用後のメインコード
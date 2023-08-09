# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re

# 「カギ開けて」「解錠して」等に反応するようにします


@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to('(open)+.*(door)+', re.IGNORECASE)
def openKeyOrder(message, *something):
    # if カギが閉まっていたら :
    message.reply(u'わかりました。解錠します。')
    # 命令を出したユーザ名を取得することもできます。
    userID = message.channel._client.users[message.body['user']][u'name']
    print(userID + 'さんの命令でカギを開けます')

# 「鍵閉めて」「施錠」等の場合はこちら


@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@respond_to(u'(施錠)+')
@respond_to('(lock)+.*(door)+', re.IGNORECASE)
def closeKeyOrder(message, *something):
    # 以下openと同じなので省略
    message.reply(u'わかりました。解錠します。')
    # 未許可なFeLiCaを許可ユーザとして追加する命令


@listen_to(u'(許可|追加)+')
@respond_to(u'(許可|追加)+')
def addUserOrder(message, *something):
    # 「」で囲まれている場合はユーザ名付きで許可する。
    m = re.search(u'「.*」', message.body['text'])
    if m:
        hit = m.group(0)
        userName = hit[1:][:-1]
        message.reply(u'わかりました。直近のインスタントユーザを「' +
                      userName + u'」として追加します。有効期限は10分間です。')
    else:
        userName = 'John Doe'
        message.reply(u'わかりました。直近のインスタントユーザを追加します。有効期限は10分間です。')

    # 該当のFeLiCaを許可ユーザに追加する処理… userAddHandler(userName, userID)

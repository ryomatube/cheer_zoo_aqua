import requests
import json

import tweepy 
import os
import datetime
import base64
import io
import traceback
import time

# Twitter APIで使用する各種キーをセット
# API Key
consumer_key = os.environ['CON_KEY'] 
# API secret key
consumer_secret = os.environ['CON_KEY_SEC']

# アクセストークン
Access_token = os.environ['ACC_KEY'] 

Access_token_secret = os.environ['ACC_KEY_SEC']

# 検索するtag
tag = "#休園中の動物園水族館"

#インスタURL
url = os.environ['URL']


def lambda_handler(event, context):
    # インスタAPIの結果を取得
    response = requests.get(url)
    data = response.json()["data"]

    #twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(Access_token, Access_token_secret)

    api = tweepy.API(auth)

    for i in data:
        try:
            # 投稿日時の確認
            datestr = json.dumps(i['timestamp'], ensure_ascii=False).replace('"',"")
            realdate = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S%z')
            diff = datetime.datetime.now(datetime.timezone.utc) - realdate

            # 現在から1時間以内の投稿なら処理
            if diff.seconds < 3600:
                # Tweet文を作成
                # 130文字に調整
                text = json.dumps(i["caption"], ensure_ascii=False)[1:130].replace(r'\n',"\r\n") + "..."
                link = json.dumps(i["permalink"], ensure_ascii=False).replace('"',"")

                # 投稿種別をチェックして画像URLを取得
                img_url = ""
                if i["media_type"] == "CAROUSEL_ALBUM":
                    for j in i["children"]["data"]:
                        if "scontent" in j['media_url']:
                            img_url = j['media_url']
                            break

                elif i["media_type"] == "IMAGE":
                    img_url = i['media_url']

                else:
                    continue

                if img_url is "":
                    continue

                f=io.BytesIO(requests.get(img_url).content)
                f.mode = 'rb'  # 読み込み専用のバイナリモードであるというように擬態する
                f.name = 'hoge.jpg'  # 拡張子さえ合っていれば問題ないと思います
                
                # 画像付き投稿
                img= api.media_upload(filename="hoge.jpg",file=f)
                api.update_status(status=text + link, media_ids=[img.media_id_string,"","",""]) # ←4枚投稿想定らしい。残り3枚を空値に
                time.sleep(30) 

        except:
            print(traceback.format_exc())
import requests
import  datetime
import json
with open("./config.json") as f:
    data = json.dumps(json.load(f))
    f.close()

url = f'''https://docs.qq.com/dop-api/get/sheet?tab=ibqp4s&_t={int(datetime.datetime.timestamp(datetime.datetime.now())*1000)}&padId=300000000$ROcHAgbvznEm&subId=3rf2s3&startrow=0&endrow=5&xsrf=526cd7ebaf365284&_r=0.9596520695516535&outformat=1&normal=1&preview_token=&nowb=1'''
header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
cookie = {
  "cookie": "pgv_pvi=3579071488; RK=dOpw68PGxH; ptcz=f9172c06620295720c2d6d116c855cf6bfaf62d5aadc2ef5e5127eea05224bed; pgv_pvid=2486531184; docMessageCenterCookie=; low_login_enable=1; fingerprint=29d88953e0b85185713c95b1a930d8ea; hashkey=f59a343c; uin=o3004044439; skey=@ug8vH3ZQK; luin=o3004044439; lskey=00010000a98f31203d44a925e282162aa4c3f3a72afc13cd0ab7f67f00a18f5c0c74f9c40514d41a4d400656; p_uin=o3004044439; pt4_token=OaRVu9ULKaf1vNpeeOCl0ynpwOvdBeQ9Cyc9GUJ6HiM_; p_skey=0nYLcZMfx-WTJp5FvyCslzvV9mVFh7yUtLd9oGwBWHE_; p_luin=o3004044439; p_lskey=00040000f0abcefb179fbcb24f23f165fd0a642d0e3c6cd9c74e9dfcd198fd644e44908a13d46e2438b1be0d; TOK=526cd7ebaf365284; has_been_login=1; uid=144115212495570955; uid_key=m5Yr%2FEYK2LWa2xzfVKKVoEuNkf13J08bIsbRx9Oo%2FwnOWAsrE%2FJENVA1OSSnHex2jiXWOGT4caq8VJLXN%2FXgYNKBYlCZoQft; utype=qq; vfwebqq=05a12fef2589eabddf031c1ba2c7be55c98664217794312a026c88339f2a0aaa54f0ea05d3b20472; loginTime=1617766890902; _qpsvr_localtk=1617787009158",
  }
data = requests.get(url=url ,headers=header,cookies = cookie ).json()
print(json.dumps(data["data"]["initialAttributedText"]["text"][0][-1][0]["c"] ))


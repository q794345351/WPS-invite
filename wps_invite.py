# !/usr/bin/env python
# coding=utf-8
import requests
import pytz
import datetime
from io import StringIO
import time

# 初始化信息
SCKEY = 'xxxxxxxxxxxxxxxxxxxxxxxx'  # '*********复制SERVER酱的SCKEY进来*************(保留引号)'
data = {
    "wps_invite": [
        {
            "name": "Zzw",
            "invite_userid": 639314372,  # "*********复制手机WPS个人信息中的用户ID进来，类似括号内容(191641526)*************(不保留双引号)",
            "sid": "V02SkhuZxsJqrNfopnijJG3s9ddavRk00a78a32400261b29c4"  # network获取wps_sid
        }
    ]
}
# 初始化日志
sio = StringIO('WPS签到日志\n\n')
sio.seek(0, 2)  # 将读写位置移动到结尾
s = requests.session()
tz = pytz.timezone('Asia/Shanghai')
nowtime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
sio.write("-" + nowtime + "-\n\n")


# APP
def pushWechat(desp, nowtime):
    ssckey = SCKEY
    send_url = 'https://sctapi.ftqq.com/' + ssckey + '.send'
    if '失败' in desp:
        params = {
            'title': 'WPS小程序邀请失败提醒' + nowtime,
            'desp': desp
        }
    else:
        params = {
            'title': 'WPS小程序邀请成功' + nowtime,
            'desp': desp
        }
    requests.post(send_url, params=params)


# 主函数
def main():
    wps_inv = data['wps_invite']
    # 这13个账号被邀请
    invite_sid = [
        "V02SEPVt7lx4JA1JnFbsejvxbz4VVJA00a56ec7a004910bd95",
        "V02SmfzVunbRzHQl-n--N-QGvCG6okQ00a7fbe37004912408e",
        "V02SmdkLCQ7q8GprgFOCV4F6GDhKVoA00a5382570034b345f2",
        "V02SKHPYCVzUdQQC2SIqMpy79q6prVs00a222a3200491249d9",
        "V02S5JoNBz4kiJyoOMCEUvx-9509bwA00ac08452004910c962",
        "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
        "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
        "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
        "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
        "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
        "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
        "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
        "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d"

    ]
    sio.write("\n\n==========wps邀请==========\n\n")
    for item in wps_inv:
        sio.write("为{}邀请---↓\n\n".format(item['name']))
        if type(item['invite_userid']) == int:
            wps_invite(invite_sid, item['invite_userid'])
        else:
            sio.write("邀请失败：用户ID错误，请重新复制手机WPS个人信息中的用户ID并修改'invite_userid'项,注意不保留双引号\n\n")
    desp = sio.getvalue()
    pushWechat(desp, nowtime)
    print(desp)
    return desp


# wps接受邀请
def wps_invite(sid: list, invite_userid: int) -> None:
    invite_url = 'http://zt.wps.cn/2018/clock_in/api/invite'
    for index, i in enumerate(sid):
        headers = {
            'sid': i
        }
        time.sleep(10)
        r = s.post(invite_url, headers=headers, data={
            'invite_userid': invite_userid})
        # sio.write("ID={}, 状态码: {}, \n\n ".format(str(index + 1).zfill(2), r.status_code))


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()

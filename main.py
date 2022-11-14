# Copyright 2022.1 by WuliAPO
# Copyright © cjlu.online . All rights reserved.

import json
import time
import requests

##https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken=67A618C7-DCF1-4BF6-A086-58F62C403DB9
# 获取AccessToken
def getAccessToken(session, openid):
    time_stamp = str(int(time.time()))  # 获取时间戳
    url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqczj.h5yunban.com%2Fqczj-youth-learning%2Findex.php&scope=snsapi_userinfo&appid=wx56b888a1409a2920&openid=" + openid + "&nickname=ZhangSan&headimg=&time=" + time_stamp + "&source=common&sign=&t=" + time_stamp
    res = session.get(url, verify=False)
    access_token = res.text[45:81]  # 比较懒，直接截取字符串了
    print("获取到AccessToken:", access_token)
    return access_token


# 获取当前最新的课程代号
def getCurrentCourse(session, access_token):
    url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current?accessToken=" + access_token
    res = session.get(url,verify=False)
    res_json = json.loads(res.text)
    if (res_json["status"] == 200):  # 验证正常
        print("获取到最新课程代号:", res_json["result"]["id"])
        return res_json["result"]["id"]
    else:
        print("获取最新课程失败！")
        print(res.text)
        exit(0)
        return None


# 签到 成功返回True，失败返回False
def getJoin(session, access_token, current_course, nid, cardNo):
    data = {
        "course": current_course,  # 大学习期次的代码，如C0046，本脚本已经帮你获取啦
        "subOrg": None,
        "nid": nid,  # 团组织编号，形如N003************
        "cardNo": cardNo  # 打卡昵称
    }
    url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/user-api/course/join?accessToken=" + access_token
    res = session.post(url, json=data)  # 特别注意，此处应选择json格式发送data数据
    print("签到结果:", res.text)
    res_json = json.loads(res.text)
    if (res_json["status"] == 200):  # 验证正常
        print("似乎签到成功了")
        return True
    else:
        print("签到失败！")
        exit(0)


if __name__ == '__main__':
    nid = "N0019000600271012"  # 在这里输入你的团组织编号，形如N003************，请使用抓包软件获取
    cardNo = "2020330301004"  # 在这里输入你打卡时用的昵称，可能是学号，可能是姓名
    openid = "oO-a2twfvA54HJ8zKzHrYZLsbok8"  # 靠自己抓包

    session = requests.session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI'
    }

    # 获取token
    time.sleep(5)
    access_token = getAccessToken(session, openid)

    # 获取最新的章节
    time.sleep(5)
    current_course = getCurrentCourse(session, access_token)

    # 签到
    time.sleep(5)
    getJoin(session, access_token, current_course, nid, cardNo)

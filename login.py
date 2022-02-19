from random import random

import requests
import re
from AES import aes_encrypt_jiekou
import math
import json
import time
import os

#用来存放学生的账号信息
students=[]    
if "yikatong" in os.environ and os.environ["yikatong"]:
    yikatong = os.environ["yikatong"]
    students=yikatong.split('&')
    print(students)


def _rds(length):
    _chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    retStr = ''
    for i in range(length):
        retStr += _chars[math.floor(random() * len(_chars))]
    return retStr


def login(username, password):
    url = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"
    req = requests.session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "newids.seu.edu.cn",
        "Origin": "https://newids.seu.edu.cn",
        "Referer": "https://newids.seu.edu.cn/authserver/login?service=https://newids.seu.edu.cn/authserver/login2.jsp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50",
    }

    response = req.get(url=url, headers=headers).text
    pattern = re.compile(r'pwdDefaultEncryptSalt = "(.+?)"', re.S)
    pattern2 = re.compile(r'name="lt" value="(.+?)"', re.S)
    # print(response)
    # 这俩参数
    pwdSalt = re.findall(pattern, response)[0]
    lt = re.findall(pattern2, response)[0]
    data = _rds(64)+password
    key = pwdSalt
    iv = _rds(16)
    print(key,iv)
    pwdEncrypt = aes_encrypt_jiekou(data, "CBC", "pkcs7padding", 128, key, iv, "base64")
    data = {
        'username': username,
        'password': pwdEncrypt,
        'lt': lt,
        'dllt': 'userNamePasswordLogin',
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': '1'
    }
    # print(pwdEncrypt)
    # print(lt)
    response2 = req.post(url=url,headers=headers,data=data,allow_redirects=False)

    req.get('http://ehall.seu.edu.cn/login?service=http://ehall.seu.edu.cn/new/index.html')

    res = req.get('http://ehall.seu.edu.cn/jsonp/userDesktopInfo.json')
    json_res = json.loads(res.text)
    try:
        name = json_res["userName"]
        print(name[0], "** 登陆成功！")
    except Exception:
        print("认证失败！")
    res=req.get("http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do?t_s="+str(int(time.time()*1000))+"&amp_sec_version_=1&gid_=cVREb3FPZlNJaFlCTUJoRUdiWmpYMVlsZTZiWVA5V2dyTm9Lem0wdHlCaWkreVNGdC92YUgzdFQ3UGNPczg5d1dmRklCbVdWT0FtWmpyNGJmczUzaXc9PQ&EMAP_LANG=zh&THEME=indigo")
    data={"userType":"TEACHER"}
    #res=req.post(url="http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/api/base/getUserDetailDB.do",data=data)

    res=req.post(url="http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/modules/dailyReport/getMyTodayReportWid.do",data={"pageNumber": "1"}).text
    #res=req.post(url=url2,data=data).text

    #获取WID
    json01=json.loads(res)
    json_data=json01["datas"]["getMyTodayReportWid"]["rows"][0]
    wid=json_data["WID"]
    need_checkin_date=json_data["NEED_CHECKIN_DATE"]
    dept_code=json_data["DEPT_CODE"]
    czrq=json_data["CZRQ"]
    USER_ID=json_data["USER_ID"]
    USER_NAME=json_data["USER_NAME"]
    DEPT_NAME=json_data["DEPT_NAME"]
    GENDER_CODE_DISPLAY=json_data["GENDER_CODE_DISPLAY"]
    GENDER_CODE=json_data["GENDER_CODE"]
    IDCARD_NO=json_data["IDCARD_NO"]
    #填报时间
    CREATED_AT = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    #对比时间，一般为前一天
    DZ_DBRQ = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))

    data2 = {
        'WID': wid,
        'NEED_CHECKIN_DATE': need_checkin_date,
        'DEPT_CODE': dept_code,
        'CZR': '',
        'CZZXM': '',
        'CZRQ': czrq,
        'CLASS_CODE': '',
        'CLASS': '',
        'DZ_DQWZ_JD': '',
        'DZ_DQWZ_WD': '',
        'DZ_DQWZ_SF': '',
        'DZ_DQWZ_CS': '',
        'DZ_DQWZ_QX': '',
        'USER_NAME_EN': '',
        'DZ_XYYYPJG_DISPLAY': '',
        'DZ_XYYYPJG': '2',
        'USER_ID': USER_ID,
        'USER_NAME': USER_NAME,
        'DEPT_NAME': DEPT_NAME,
        'GENDER_CODE_DISPLAY': GENDER_CODE_DISPLAY,
        'GENDER_CODE': GENDER_CODE,
        'PHONE_NUMBER': '',
        'IDCARD_NO': IDCARD_NO,
        'LOCATION_DETAIL': '',
        'EMERGENCY_CONTACT_PERSON': '',
        'EMERGENCY_CONTACT_PHONE': '',
        'EMERGENCY_CONTACT_NATIVE': '',
        'EMERGENCY_CONTACT_HOME': '',
        'HEALTH_STATUS_CODE_DISPLAY': '正常',
        'HEALTH_STATUS_CODE': '001',
        'HEALTH_UNSUAL_CODE': '',
        'IS_SEE_DOCTOR_DISPLAY': '',
        'IS_SEE_DOCTOR': '',
        'SAW_DOCTOR_DESC': '',
        'MEMBER_HEALTH_STATUS_CODE_DISPLAY': '',
        'MEMBER_HEALTH_STATUS_CODE': '',
        'MEMBER_HEALTH_UNSUAL_CODE': '',
        'MENTAL_STATE': '',
        'RYSFLB': 'YJS',
        'DZ_JSDTCJTW': '36.6',
        'DZ_DTWJTW': '',
        'DZ_DTWSJCTW': '',
        'DZ_SZWZLX_DISPLAY': '在校内',
        'DZ_SZWZLX': '002',
        'DZ_SZWZ_GJ_DISPLAY': '',
        'DZ_SZWZ_GJ': '',
        'DZ_SZWZXX': '',
        'DZ_MQZNJWZ': '',
        'DZ_SZXQ_DISPLAY': '九龙湖校区',
        'DZ_SZXQ': '002',
        'LOCATION_PROVINCE_CODE_DISPLAY': '',
        'LOCATION_PROVINCE_CODE': '',
        'LOCATION_CITY_CODE_DISPLAY': '',
        'LOCATION_CITY_CODE': '',
        'LOCATION_COUNTY_CODE_DISPLAY': '',
        'LOCATION_COUNTY_CODE': '',
        'DZ_SFGL_DISPLAY': '否',
        'DZ_SFGL': '001',
        'DZ_WD': '',
        'DZ_GLKSSJ': '',
        'DZ_GLJSSJ': '',
        'DZ_GLDQ_DISPLAY': '',
        'DZ_GLDQ': '',
        'DZ_GLDSF_DISPLAY': '',
        'DZ_GLDSF': '',
        'DZ_GLDCS_DISPLAY': '',
        'DZ_GLDCS': '',
        'DZ_GLSZDQ': '',
        'DZ_MQSFWYSBL_DISPLAY': '否',
        'DZ_MQSFWYSBL': '0',
        'DZ_YSGLJZSJ': '',
        'DZ_YS_GLJZDSF_DISPLAY': '',
        'DZ_YS_GLJZDSF': '',
        'DZ_YS_GLJZDCS_DISPLAY': '',
        'DZ_YS_GLJZDCS': '',
        'DZ_MQSFWQRBL_DISPLAY': '否',
        'DZ_MQSFWQRBL': '0',
        'DZ_QZGLJZSJ': '',
        'DZ_QZ_GLJZDSF_DISPLAY': '',
        'DZ_QZ_GLJZDSF': '',
        'DZ_QZ_GLJZDCS_DISPLAY': '',
        'DZ_QZ_GLJZDCS': '',
        'DZ_SFYJCS1_DISPLAY': '无',
        'DZ_SFYJCS1': '0',
        'DZ_ZHLKRQ': '',
        'DZ_SFYJCS2_DISPLAY': '无',
        'DZ_SFYJCS2': '0',
        'DZ_GRYGLSJ1': '',
        'DZ_ZHJCGRYSJ1': '',
        'DZ_SFYJCS3_DISPLAY': '无',
        'DZ_SFYJCS3': '0',
        'DZ_ZHJCGRYSJ2': '',
        'DZ_SFYJCS4_DISPLAY': '无',
        'DZ_SFYJCS4': '0',
        'DZ_JJXFBSJ': '',
        'DZ_JJXFBD_SF_DISPLAY': '',
        'DZ_JJXFBD_SF': '',
        'DZ_JJXFBD_CS_DISPLAY': '',
        'DZ_JJXFBD_CS': '',
        'DZ_BRYWYXFH_DISPLAY': '',
        'DZ_BRYWYXFH': '',
        'DZ_JCQKSM': '',
        'DZ_JRSFFS_DISPLAY': '无',
        'DZ_JRSFFS': '0',
        'DZ_TWDS': '',
        'DZ_JRSTZK_DISPLAY': '无',
        'DZ_JRSTZK': '001',
        'DZ_SMJTQK': '',
        'DZ_SFYJCS5_DISPLAY': '无',
        'DZ_SFYJCS5': '0',
        'DZ_YJZCDDGNRQ': '',
        'DZ_SFYJCS7_DISPLAY': '无',
        'DZ_SFYJCS7': '0',
        'DZ_ZHJCGGRYSJ': '',
        'DZ_SFYJCS8_DISPLAY': '无',
        'DZ_SFYJCS8': '0',
        'DZ_JTQY_DISPLAY': '',
        'DZ_JTQY': '',
        'DZ_SFYJCS9_DISPLAY': '无',
        'DZ_SFYJCS9': '0',
        'DZ_SFYJCS10_DISPLAY': '无',
        'DZ_SFYJCS10': '0',
        'DZ_YWQTXGQK_DISPLAY': '无',
        'DZ_YWQTXGQK': '0',
        'DZ_QKSM': '',
        'DZ_JRSFYXC_DISPLAY': '无',
        'DZ_JRSFYXC': '0',
        'DZ_MDDSZSF_DISPLAY': '',
        'DZ_MDDSZSF': '',
        'DZ_MDDSZCS_DISPLAY': '',
        'DZ_MDDSZCS': '',
        'DZ_JTFS_DISPLAY': '',
        'DZ_JTFS': '',
        'DZ_CCBC': '',
        'DZ_SFDXBG_DISPLAY': '',
        'DZ_SFDXBG': '',
        'DZ_SYJTGJ': '',
        'DZ_SDXQ': '',
        'DZ_YMJZRQ1': '2021-04-13',
        'DZ_YMJZD1': '东南大学体育馆',
        'DZ_YMJZRQ2': '2021-05-28',
        'DZ_YMJZD2': '东南大学体育馆',
        'DZ_WJZYMYY_DISPLAY': '',
        'DZ_WJZYMYY': '',
        'DZ_WJZYMQTYY': '',
        'REMARK': '',
        'CREATED_AT': CREATED_AT,
        'DZ_DBRQ': DZ_DBRQ,
        'DZ_SFYBH': '0',
        'DZ_SFLXBXS': '',
        'DZ_ZDYPJG': '',
    }
    res=req.post(url="http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/modules/dailyReport/T_REPORT_EPIDEMIC_CHECKIN_SAVE.do",data=data2)
    return res.text


    # print(wid)
    # print(need_checkin_date)
    # print(dept_code)
    # print(czrq)
    # print(USER_ID)
    # print(USER_NAME)
    # print(DEPT_NAME)
    # print(GENDER_CODE_DISPLAY)
    # print(GENDER_CODE)
    # print(IDCARD_NO)






#login("卡号", '密码')
for item in students:
    cardNumber=item.split(":")[0]
    pwd=item.split(":")[1]
    # print(cardNumber)
    # print(pwd)
    response=login(cardNumber,pwd)
    if('T_REPORT_EPIDEMIC_CHECKIN_SAVE":1' in response):
        print("恭喜"+cardNumber+",上报成功!")
    else:
        print(cardNumber+"上报失败!")


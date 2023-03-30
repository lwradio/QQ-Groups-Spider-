import requests
from PIL import Image
import time
import re

from main import send_email


def scanandgetcookie():
    qrsig = QR()
    n = len(qrsig)
    i = 0
    e = 0
    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1
    ptqrtoken = 2147483647 & e
    cookie = cookies(qrsig, ptqrtoken)
    ck = cookie[0]
    return ck

def bkn(Skey):
    t = 5381
    n = 0
    o = len(Skey)
    while n < o:
        t += (t << 5) + ord(Skey[n])
        n += 1
    return t & 2147483647


def ptqrtoken(qrsig):
    n = len(qrsig)
    i = 0
    e = 0
    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1
    return 2147483647 & e


# 获取二维码的qrsig
def QR():
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=715030901&e=2&l=M&s=3&d=72&v=4&t=0.' + str(
        time.time()) + '&daid=73&pt_3rd_aid=0'
    r = requests.get(url)
    qrsig = requests.utils.dict_from_cookiejar(r.cookies).get('qrsig')
    with open(r'D:\files\QR.png', 'wb') as f:
        f.write(r.content)
    im = Image.open(r'D:\files\QR.png')
    im = im.resize((350, 350))
    print('登录二维码获取成功', time.strftime('%Y-%m-%d %H:%M:%S'))
    send_email('cookie过期', '重新登录', r'D:\files\QR.png')
    im.show()
    return qrsig


# 通过qrsig查询是否已经扫码
def cookies(qrsig, ptqrtoken):
    while 1:
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqun.qq.com%2Fmanage.html%23click&ptqrtoken=' + str(
            ptqrtoken) + '&ptredirect=1&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-' + str(
            time.time()) + '&js_ver=20032614&js_type=1&login_sig=&pt_uistyle=40&aid=715030901&daid=73&'
        cookies = {'qrsig': qrsig}
        r = requests.get(url, cookies=cookies)
        r1 = r.text
        if '二维码未失效' in r1:
            print('二维码未失效', time.strftime('%Y-%m-%d %H:%M:%S'))
        elif '二维码认证中' in r1:
            print('二维码认证中', time.strftime('%Y-%m-%d %H:%M:%S'))
        elif '二维码已失效' in r1:
            print('二维码已失效', time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print('登录成功', time.strftime('%Y-%m-%d %H:%M:%S'))
            cookies = requests.utils.dict_from_cookiejar(r.cookies)
            uin = requests.utils.dict_from_cookiejar(r.cookies).get('uin')
            regex = re.compile(r'ptsigx=(.*?)&')
            sigx = re.findall(regex, r.text)[0]
            url = 'https://ptlogin2.qun.qq.com/check_sig?pttype=1&uin=' + uin + '&service=ptqrlogin&nodirect=0&ptsigx=' + sigx + '&s_url=https%3A%2F%2Fqun.qq.com%2Fmanage.html&f_url=&ptlang=2052&ptredirect=101&aid=715030901&daid=73&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0'
            r2 = requests.get(url, cookies=cookies, allow_redirects=False)
            targetCookies = requests.utils.dict_from_cookiejar(r2.cookies)
            skey = requests.utils.dict_from_cookiejar(r2.cookies).get('skey')
            break
        time.sleep(3)
    return targetCookies, skey


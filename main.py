import urllib3
from requests import post
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By

def hash33_bkn(skey):
    e = skey
    t = 5381

    for n in range(0,len(e)):
        t += (t << 5) + ord(e[n])

    return 2147483647 & t
# post访问网页
def post_html(url, submit_cookies, submit_data):
    # 设置请求头,模拟人工
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://find.qq.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Referer': 'https://qun.qq.com/member.html'
    }
    # 屏蔽https证书警告
    urllib3.disable_warnings()

    # 网页访问,post方式
    html = post(url, data=submit_data, cookies=submit_cookies, headers=header, verify=False)

    return html


def get_cookie():
    # 创建一个Chrome浏览器实例
    driver = webdriver.Chrome()
    # 访问QQ登录页面
    driver.get("https://qzone.qq.com/")
    # 等待页面加载完成
    time.sleep(5)
    # 切换到登录框所在的iframe
    driver.switch_to.frame("login_frame")
    # 点击“账号密码登录”按钮
    driver.find_element(By.ID, "switcher_plogin").click()
    # 输入QQ号和密码
    driver.find_element(By.ID, "u").send_keys("1579704169")
    driver.find_element(By.ID, "p").send_keys("liuwei19990615++")
    # 点击“登录”按钮
    driver.find_element(By.ID, "login_button").click()
    # 等待登录完成并获取Cookie
    time.sleep(10)
    cookie = driver.get_cookies()
    # 关闭浏览器
    driver.quit()
    return cookie


def get_group_info():
    url = "https://qun.qq.com/cgi-bin/group_search/pc_group_search"
    # 获取Cookie
    # cookie = get_cookie()
    # 将Cookie添加到请求头部
    cookie = {"pgv_pvid": "525508410",
              "tvfe_boss_uuid": "409920210831054a",
              "RK": "2qFFFBtNf1",
              "ptcz": "6b60fe8703f618a59245b5832c3356a2c29d827a71e19449c5f09220af420c18",
              'traceid': 'f8a8dbe5a3',
              'p_uin': 'o1579704169',
              "_qpsvr_localtk": "0.6904930856141818",
              "ptui_loginuin": "1579704169",
              "uin": "o1579704169",
              "skey": "@sB8GVVT5o",
              'pt4_token': '-bbYaBdB1YkHC7t*PQJnZiJsqMsUXE6G8zPA5imF2mc_',
              'p_skey': 'DJQL99eP19i8zUmfkjbj8xc990BLFi6-kc4Nt4AYn-0_'
              }
    bkn = hash33_bkn(cookie['skey'])
    data = {
        "k": "交友",
        "n": "8",
        "st": "1",
        "iso": "1",
        "src": "1",
        "v": "4903",
        "bkn": bkn,
        "isRecommend": "false",
        "city_id": "0",
        "from": "1",
        "newSearch": "true",
        "penetrate": "",
        "keyword": "17257021",
        "sort": "0",
        "wantnum": "24",
        "page": "0",
        "ldw": bkn
    }
    response = post_html(url,cookie,data)
    # response = requests.post(url, headers=headers, data=data)
    print(response.text)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    get_group_info()

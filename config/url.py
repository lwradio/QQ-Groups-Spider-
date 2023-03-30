import urllib3
from requests import post
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




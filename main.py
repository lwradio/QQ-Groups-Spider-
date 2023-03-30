import json
from datetime import datetime

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from config import login

from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText

from config.url import post_html

cookie = None


def dosearch(number):
    global cookie
    url = 'https://qun.qq.com/cgi-bin/group_search/pc_group_search'
    data = {
        "k": "交友",
        "n": "8",
        "st": "1",
        "iso": "1",
        "src": "1",
        "v": "4903",
        # "bkn": bkn,
        "isRecommend": "false",
        "city_id": "0",
        "from": "1",
        "newSearch": "true",
        "penetrate": "",
        "keyword": number,
        "sort": "0",
        "wantnum": "24",
        "page": "0",
        # "ldw": bkn
    }
    response = post_html(url, cookie, data)

    return response


def send_email(subject, content, attachment_path=None):
    # 发件人邮箱
    sender = ''
    # 发件人邮箱的SMTP授权码
    password = ''
    # 收件人邮箱
    receiver = ''

    # 创建一个带附件的邮件实例
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # 添加邮件内容
    text = MIMEText(content)
    msg.attach(text)

    if attachment_path is not None:
        # 添加附件
        with open(attachment_path, 'rb') as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename='q.jpg')
            msg.attach(attachment)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receiver, msg.as_string())
        smtp_server.quit()
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败：', e)


# cookie错误Jason信息{"ec":4,"errcode":0,"em":"user err [errcode:4:0]"}
# 查找到记录{"ec":0,"errcode":0,"em":"","keywordSuicide":0,"exactSearch":1,"gTotal":1,"endflag":1,"penetrate":"eyJwb3MiOjAsInAiOiJ7XCJyZWNvbW1lbmRcIjp0cnVlfSJ9","usr_cityid":null,"exact":1,"group_list":[{"code":17257021,"owner_uin":48138926,"name":"01\u670d\u8bbe\u5de5\u827a","class":10009,"class_text":"","dist":null,"face":0,"flag":16794625,"flag_ext":1073938752,"geo":null,"gid":486257021,"latitude":"0","level":0,"longitude":"0","max_member_num":500,"member_num":10,"group_label":[{"item":"\u76f8\u518c\u591a","type":3,"text_color":"ffffff","edging_color":"00cafc"},{"item":"\u7ba1\u7406\u5458\u6d3b\u8dc3","type":3,"text_color":"ffffff","edging_color":"c573ff"},{"item":"\u7537\u751f\u591a","type":3,"text_color":"ffffff","edging_color":"ff80ca"}],"memo":"\u53ea\u9650\u672c\u73ed\u4eba\u52a0\u5165\uff01\u8bf7\u4e0d\u662f\u8bef\u4e71\u52a0","richfingermemo":"","option":2,"app_privilege_flag":224,"url":"http:\/\/p.qlogo.cn\/gh\/17257021\/17257021\/140","calc":null,"join_auth":"agABejb4mSzAxs3aTiLpLGNad4b9E\/DfXxWBZbe8\/l31GnVzqIv1P5wpfTGRDtDM","certificate_type":0,"certificate_name":"","bitmap":1024,"uin_privilege":-1,"activity":0,"cityid":null,"qaddr":[""]}]}
# 没有记录json {"ec":0,"errcode":0,"em":"","keywordSuicide":0,"exactSearch":0,"gTotal":null,"endflag":1}
# 目标qq群
# QQ群①：704381689（加满截止）
# QQ群②：850359301（加满截止）
# QQ群③：838157459（加满截止）
# QQ群④：771462815（加满截止）
# QQ群⑤：285821333（加满截止）
# QQ群⑥：232094620（加满截止）
def job():
    global cookie
    json1 = dosearch('704381689').json()
    json2 = dosearch('850359301').json()
    json3 = dosearch('838157459').json()
    json4 = dosearch('771462815').json()
    json5 = dosearch('285821333').json()
    json6 = dosearch('232094620').json()
    print('qq1' + json.dumps(json1))
    print('qq2' + json.dumps(json2))
    print('qq3' + json.dumps(json3))
    print('qq4' + json.dumps(json4))
    print('qq5' + json.dumps(json5))
    print('qq6' + json.dumps(json6))
    em1 = json1['em']
    em2 = json2['em']
    em3 = json3['em']
    em4 = json4['em']
    em5 = json5['em']
    em6 = json6['em']

    if any([em1 != '', em2 != '', em3 != '', em4 != '', em5 != '', em6 != '']):
        cookie = login.scanandgetcookie()
        json1 = dosearch('704381689').json()
        json2 = dosearch('850359301').json()
        json3 = dosearch('838157459').json()
        json4 = dosearch('771462815').json()
        json5 = dosearch('285821333').json()
        json6 = dosearch('232094620').json()
    if json1.get('gTotal') is not None:
        send_email('704381689', '群可查找到')
    elif json2.get('gTotal') is not None:
        send_email('850359301', '群可查找到')
    elif json3.get('gTotal') is not None:
        send_email('838157459', '群可查找到')
    elif json4.get('gTotal') is not None:
        send_email('771462815', '群可查找到')
    elif json5.get('gTotal') is not None:
        send_email('285821333', '群可查找到')
    elif json6.get('gTotal') is not None:
        send_email('232094620', '群可查找到')
    else:
        print('查找失败')


if __name__ == '__main__':
    cookie = login.scanandgetcookie()
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=30, next_run_time=datetime.now())
    # scheduler.add_job(job, 'interval', minutes=1, next_run_time=datetime.now())
    scheduler.start()

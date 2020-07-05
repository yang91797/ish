import requests
import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import logging
import time

number = 0


def logger():

    logger = logging.getLogger()            # # 参数为记录器名称，没有参数默认为root
    if not logger.handlers:  # 这里进行判断，如果logger.handlers列表为空，则添加,否则直接返回logg对象
        fh = logging.FileHandler('./logger2')      # 写入文件
        sh = logging.StreamHandler()             # 屏幕显示
        logger.setLevel(logging.INFO)       # 设置全局输出等级，默认为WARNING
        fm = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        logger.addHandler(fh)       # 添加到文件
        logger.addHandler(sh)       # 对应信息流向屏幕

        fh.setLevel(logging.DEBUG)               # 设置写入文件的日志等级
        sh.setLevel(logging.ERROR)               # 设置流向屏幕的日志等级
        fh.setFormatter(fm)
        sh.setFormatter(fm)

    return logger


def ping(number):
    number += 1
    res = requests.post(

        url="https://ishdf.com/wxapi/userinfo/check-reg/",
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": "14",
            "IdMd5": "oO93r4nQsfdl4_YlC3OWD4kUUWb8"
        }
    )
    code = res.status_code

    if number > 5:
        send_email("管理员", "573812718@qq.com", "服务器挂啦，赶快去看看吧")
        return

    if code == 502:
        ps = subprocess.Popen('ps aux |grep uwsgi |grep -v "grep" |grep -v "tailf"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = ps.stdout
        for line in stdout:
            content_str = str(line, encoding="utf-8")
            print(content_str, "?")
            sep = re.compile('[\s]+')
            content_list = sep.split(content_str)
            print(content_list, "??")
            uid = content_list[1]
            cmd = 'kill -9 %s' % uid
            kill = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
            kill.wait()

        res = subprocess.Popen("/usr/local/python3/bin/uwsgi --ini /etc/uwsgi/uwsgi.ini", stdout=subprocess.PIPE,
                                                                        stderr=subprocess.PIPE, shell=True)
        res.wait()
        for i in res.stdout:
            print(i, "???")
        for i in res.stderr:
            print(i, "????")

        log = logger()
        log.info("服务器重启")
        ping(number)


def send_email(username, my_user, content):
    my_sender = 'Aaron5718@163.com'  # 发件人邮箱账号
    # my_user = '573812718@qq.com'  # 收件人邮箱账号

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(['Aaron', my_sender])  # 括号里的对应发件人邮箱昵称(可以为空)、发件人邮箱账号

    msg['To'] = formataddr([username, my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号

    msg['Subject'] = '服务器状态通知'  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL('smtp.163.com', 465)  # 发送邮件服务器和端口号（qq服务器好像是smtp.163.com）
    server.login(my_sender, "19941113yxd")

    # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.sendmail(my_sender, my_user, msg.as_string())
    server.quit()  # 关闭连接


ping(number)

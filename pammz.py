import requests
from bs4 import BeautifulSoup
import bs4
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','referer': 'https://www.mzitu.com/japan/'}   #模拟浏览器操作


def emailtx(text):
    # 邮件的内容
    mail_msg = """
         <h2 style="color:#f00"> 自动发送的邮件</h2>
         <p><a href="https://user.qzone.qq.com/2681808375">这是一个超链接</a>
         <p><<""" + text  +""" >>已经下载完成了，请注意查看哦</p>

                  """
    message = MIMEText(mail_msg, 'html', 'utf-8')

    # 发件人名字，可以自由填写
    message['From'] = Header('你的邮箱小助手吖', 'utf-8')
    # 收件人名字 ，可以自由填写
    message['To'] = Header('坏狗i', 'utf-8')

    # 邮件标题
    subject = '这是233自动发送的邮件哦！！'
    message['Subject'] = Header(subject, 'utf-8')

    # 发送方地址
    sender = '770045655@qq.com'
    # 接收方地址，可以是多个地址
    receivers = ['2681808375@qq.com']

    # 使用qq邮箱的服务，发送邮件
    smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtpObj.login(sender, 'sbptiwwgluqkbedf')  # 登录 地址 授权码
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    smtpObj.quit()  # 关闭
    print('邮件发送成功')

def save_file(rod, url):  # 保存文件函数
    try:
        path = rod + '//' + url.split('/')[-1]      #文件输出路径
        if not os.path.exists(rod):                 #不存在就创建
            os.makedirs(rod)
        if not os.path.exists(path):                #文件是否存在
            r = requests.get(url, headers=header , timeout = 30)   #get网页内容
            with open(path, 'wb') as f:             #打开文件路径以二进制写入的方式打开
                f.write(r.content)                  #写入二进制文件
                print('下载成功')
        else:
            print('文件已经存在')
    except:
        print('爬取失败')



def GETHTLMTEXT(url):      #获取html函数
    try:
        r = requests.get(url, headers=header, timeout=30)  # timeout 链接超时时间我设定是30 你们可以自己改
        r.raise_for_status()
        r.encoding = r.apparent_encoding         #自动获取编码格式
        return r.text                            #以文本方式写出
    except:
        return ''


def filluniuclist(html):   #取出组
    try:
        soup = BeautifulSoup(html, 'html.parser')        #熬一锅汤
        for tr in soup.find( id = 'pins').descendants:             # 把解析内容里的id为pins的内容遍历出来
            if isinstance(tr, bs4.element.Tag):                    #判断 tr==tag
                for td in tr.find_all('a'):                        #从tr中找到a标签
                    for tds in td.find_all('img'):                     #从a标签中找到img标签
                        for tg in tr.find_all('span'):             #从tr中找到span标签
                            for tgs in tg.find_all('a'):               #从span标签中找到a标签
                                text = tds.get('alt')              #把img标签中的alt的值赋值给text
                                print(tgs.get('href'))
                                urls = tgs.get('href')             #从span的a标签中href属性的值传递给urls
                                print(text)                        #打印显示要下载的名字
                                emailtx(text)
                                path = 'd://图片//' + text         #名字加到路径后
                                url = tds.get('data—original')     #将图片的地址(data_original属性中)传递给url
                                print(url)                         #打印图片的地址
                                save_file(path,url)                #调用文件保存函数
                                get_gir(path,urls)                 #

    except:
        return '未知错误'


def get_gir(path,url):#打印组中的图片
    num = 1
    dn = 1
    try:
        while True:
            ulrs = url + '/{:0>2d}'.format(num)
            num += 1
            dn +=1
            hm = GETHTLMTEXT(ulrs)
            print(url)
            print('当前下载数：', dn)
            end = get_jpg(hm, path)
            if end == 1:
                break
    except:
        return '未知错误!'


def get_jpg(html,path):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for tr in soup.p():
            for retn_jpg in tr.find_all('img'):
                JPG = retn_jpg.get('src')
                save_file(path, JPG)
                print(retn_jpg.get('src'))
        for m in soup.find_all('a'):
            for sy in m.find_all('span'):
                if sy.string == '下一组»':
                    return 1
    except:
        return '一个未知的错误'


def main():  # 主函数
    num = 1
    while num <= 240:
        url = 'https://www.mzitu.com/page/%d' %num    #循环传入传入的url
        html = GETHTLMTEXT(url)                       #获取html
        filluniuclist(html)                           #倒列出需要的资源

        num +=1




main()

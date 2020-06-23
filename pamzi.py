import requests
import os
import time
num = 1
def pamm(num):
    url = 'https://i3.mmzztt.com/2020/03/29a{:02d}.jpg'.format(num)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','referer':'https://www.mzitu.com/xinggan/'}
    root = 'd://图片//天然e'
    path = root + url.split('/',)[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            res = requests.get(url, headers=header)
            with open(path,'wb') as f:
                f.write(res.content)
                print('下载成功')
        else:
            print('该文件已经存在')
    except:
        print('下载失败')
while num<=60:
    pamm(num)
    num+=1
    time.sleep(0.3)



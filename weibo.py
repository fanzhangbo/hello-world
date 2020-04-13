import requests
import random
import os
import re
import json
import time

#user_agent 集合
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]


def execute(req_url):
    #随机选择一个
    user_agent = random.choice(user_agent_list)
    #传递给header
    headers = { 'User-Agent': user_agent }
    try:
        content = requests.get(req_url, headers=headers).content.decode(errors='ignore')
    except:
        print("网络出错")
        return
    json_data=json.loads(content)
    cards = json_data['data']['cards']
    for item in cards:
        mblog = item['mblog']
        title = mblog['text']
        title_sp = title.split("<")
        
        real_title = title_sp[0].replace(".", "").replace(":", "_")
        print(real_title)
        dir_path = real_title
        try:
            os.mkdir(dir_path)
        except:
            print("该贴已下载")
            continue
        
        if 'pics' in mblog.keys():
            pics_list = mblog['pics']
        else:
            pics_list = mblog['retweeted_status']['pics']
            
        for pic in pics_list:
            try:
                pic_url = pic['url']
                img_name = pic_url.split('/')
                pic_path = dir_path + '/' + img_name[-1]
                
                if os.path.isfile(pic_path):
                    print("{} 已存在".format(img_name[-1]))
                    pass
                else:
                    img_data = requests.get(pic_url,headers =headers)
                    # 延时
                    time.sleep(random.randint(1, 10))
                    with open(pic_path, 'wb')as f:
                        f.write(img_data.content)
                        print("正在保存 {}".format(img_name[-1]))
                        f.close()
            except:
                pass
                
                

req_url = ""

while True:
    t = random.randint(75, 200)
    print(str(t) + "s 开始执行")
    time.sleep(t)
    
    execute(req_url)
# coding:utf-8
import os
import requests



headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }


def get_url_content(m3u8_url):
    
    m3u8_res = requests.get(m3u8_url, headers = headers)
    print(m3u8_res)
    m3u8_content = m3u8_res.content.decode('utf8')
    lines_list = m3u8_content.strip().split('\r\n')
    if len(lines_list) < 3:
        lines_list = m3u8_content.strip().split('\n')
    real_ts = lines_list[-1]

    m3u8_list = m3u8_url.strip().split('/')
    m3u8_list[-1] = real_ts
    real_m3u8 = '/'.join(m3u8_list)
    m3u8_content = requests.get(real_m3u8, headers = headers).content.decode('utf8')
    return m3u8_content, real_m3u8


def read_m3u8(m3u8_content):
    media_url_list = []
    lines_list = m3u8_content.strip().split('\r\n')
    if len(lines_list) < 3:
        lines_list = m3u8_content.strip().split('\n')
    for index,line in enumerate(lines_list):
        #print(index,line)
        if '#EXTINF' in line:
            media_url_list.append(lines_list[index+1])
    return media_url_list

def download_media(url_list, real_m3u8, dir_path, file_name):
    real_m3u8_arr = real_m3u8.strip().split('/')
    for index,url in enumerate(url_list):
        real_m3u8_arr[-1] = url
        target_url = '/'.join(real_m3u8_arr)
        res = requests.get(target_url, headers)
        print('url:'+url)
        print('target_url:'+target_url)
        if res.status_code != 200:
            print('下载url连接访问失败')
            break
        with open(dir_path + file_name, 'ab') as f:
            f.write(res.content)
        print('下载进度：%.1f%%' % ((index+1)/len(url_list)*100))
    flag = False
    if index == len(url_list) - 1:
        flag = True
    return flag

def main():
    origin_url = input('请输入m3u8连接地址:')
    dir_path = input('请输入保存路径:')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    file_name = input('请输入文件名：')
    # 获取ts文件
    m3u8_content, real_m3u8 = get_url_content(origin_url)
    print(m3u8_content)
    # 获取ts连接列表
    media_url_list = read_m3u8(m3u8_content)
    print(media_url_list)
    # 下载ts媒体文件
    flag = download_media(media_url_list, real_m3u8, dir_path, file_name)
    if flag:
        print('媒体下载完成')
    else:
        print('媒体下载失败')
    print("*"*16)

if __name__ == '__main__':
    main()








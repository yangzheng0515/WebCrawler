# -*- coding:utf-8 -*-

# 2 图片的储存
from urllib import request
from bs4 import BeautifulSoup
import sys
import io
import re
import time
import os

def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    req = request.Request(url, headers = headers)
    page = request.urlopen(req).read().decode('utf-8')
    return page

def get_img_links(page):
    soup = BeautifulSoup(page, 'html.parser')
    # Beautiful Soup和正则表达式结合，提取出所有图片的链接（img标签中，class=**，以.jpg结尾的链接）
    img_links = soup.find_all('a', 'shutterset_7581971b34cffb10a90160cf009d802d', href = re.compile(r'.jpg$'))
    return img_links

def download_img(img_links):
    # 设置保存的路径，否则会保存到程序当前路径
    # 注意这里要提前建立文件夹
    local_path = './爬虫_test3_2'
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    #local_path = r'E:\Python\Python 3 爬虫学习笔记\爬虫_test3_2'
    for img_link in img_links:
        print(img_link.attrs['href'])
        # 保存链接并命名，time防止命名冲突
        request.urlretrieve(img_link.attrs['href'], local_path + r'\%s.jpg' % time.time())

def main():
    url = r'http://www.oxsy.ro/blog/remember-robocup-2016-leipzig/'
    page = get_page(url)
    img_links = get_img_links(page)
    download_img(img_links)

if __name__ == '__main__':
    main()


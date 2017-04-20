# -*- coding:utf-8 -*-

# 四 将爬取的信息存储到本地
# 1 对.txt文件的操作
from urllib import request
from bs4 import BeautifulSoup
import sys
import io

def get_pages(url, page_num):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}  
    pages = []

    for num in range(page_num+1):
        if num == 1:
            print(url)
            req = request.Request(url, headers = headers)
            page = request.urlopen(req).read().decode('utf-8')
            pages.append(page)
        elif num == 0:
        	pass
        else:
            url_temp = url + 'page/' + str(num) + '/'
            print(url_temp)
            req = request.Request(url_temp, headers = headers)
            page = request.urlopen(req).read().decode('utf-8')
            pages.append(page)
    return pages

def get_titles(pages):
    titles = []
    for each in pages:
        soup = BeautifulSoup(each, 'html.parser')
        titles.append(soup.find_all('a', 'article-title'))
    return titles

def save_titles(titles):
    try:
        file = open(sys.path[0] + r'\爬虫_test3_1.txt', 'w')	#sys.path[0]当前文件路径
        for each in titles:
            for title in each:
                file.write(title.string + '\n')
    finally:
        if file:
            file.close()

    # with open(sys.path[0] + r'\爬虫_test3_1.txt', 'w') as file:
    #     for each in titles:
    #         for title in each:
    #             file.write(title.string + '\n')
 

def download_titles():
    url = r'http://twilight.net.cn/'
    page_num = 2 #目前只有6页
    pages = get_pages(url, page_num)
    titles = get_titles(pages)
    save_titles(titles)

if __name__ == '__main__':
    download_titles()
import json
import os
import re
from hashlib import md5
import pymongo
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests import RequestException
from multiprocessing import Pool



def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    try:
        url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取索引页出错')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            # print(item.get('article_url'))
            yield item.get('article_url')


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except RequestException:
        print('获取详情页出错', url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    #print(title)
    image_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(image_pattern, html)
    if result:
        # print(result.group(1))  # json格式
        data = json.loads(result.group(1)) # 将josn字符串转化成json对象
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }

def save_to_mongo(result):
    # db[MONGO_DB].drop()
    if db[MONGO_DB].insert(result):
        print('成功存储到MongoDB ', result)
        return True
    else:
        return False


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)  # 不能是text
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()



def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result:
                save_to_mongo(result)


# config
MONGO_URL = 'localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'toutiao'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
KEYWORD = '街拍'
GROUP_START = 1
GROUP_ENG = 20


if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START, GROUP_ENG + 1)]
    pool = Pool()
    pool.map(main, groups)

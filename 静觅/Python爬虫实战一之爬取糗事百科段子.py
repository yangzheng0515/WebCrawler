#coding:utf-8
import urllib.request
import re
import time

def craw(page):
	url = r'http://www.qiushibaike.com/page/' + str(page) + '/'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = urllib.request.Request(url, headers = headers)
	content = urllib.request.urlopen(request).read().decode('utf-8')
	pattern = re.compile('<div class="article block untagged mb15".*?<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</a>(.*?)<div class="stats">.*?<i class="number">(.*?)</i>.*?<span class="dash">.*?<i class="number">(.*?)</i>', re.S)
	items = re.findall(pattern, content)
	for item in items:
	    print('发布者：' + item[0])
	    print('内容：' + item[1])
	    print('好笑：' + item[3])
	    print('评论：' + item[4])
	 #   print("item[2]" + item[2])
	    print('   ')


def main():
	for i in range(1,35):
		craw(i)
		time.sleep(5)  # 有效避免被屏蔽，可以使用代理
		#print(i)

if __name__ == '__main__':
	main()
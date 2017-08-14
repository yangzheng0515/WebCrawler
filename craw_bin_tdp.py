# _*_ coding:utf-8 _*_
'''
author: yz
time: 2017/3/2
从http://chaosscripting.net/files/competitions/RoboCup/WorldCup/ 中爬取RoboCup2d近二十年来的TDP和Binary
需要：
Python3
需要下载bs4库 sudo apt-get install python3-bs4
使用：
可在main中设置下载bin还是tdp
可在init_download_bins、init_download_tdps函数中设置需要下载的年份
可能因网络或其他原因导致下载不完全，可在不改变目录的情况下执行几次

time: 2017/8/15 修复
网址更新为 http://archive.robocup.info/soccer/simulation/2D/
但网页结构没变，简单的修复就可以了，发现以前写的代码惨不忍睹
显示下载进度
多进程爬取，提高爬取速度
'''

import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re, os, socket, sys
from multiprocessing import  Pool

# 下载进度
def report(count, blockSize, totalSize):
  percent = int(count*blockSize*100/totalSize)
  sys.stdout.write("\r%d%%" % percent + ' complete')
  sys.stdout.flush()

# 得到需要下载的可执行的URL
def get_bin_urls(page):
	url = 'http://archive.robocup.info/soccer/simulation/2D/binaries/RoboCup/{}/'.format(str(page))
	# url = r'http://chaosscripting.net/files/competitions/RoboCup/WorldCup/' + str(page) + '/2DSim/binaries/'
	headers = {'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = urllib.request.Request(url, headers = headers)
	try:
		content = urllib.request.urlopen(request, timeout = 30).read().decode('utf-8')
	except:
		print('the first crawl failed, try crawl second times')
		try:
			content = urllib.request.urlopen(request, timeout = 20).read().decode('utf-8')
		except:
			print('the second crawl failed')
			return None
	if content is None:
		print('URL is not found!')
		return None
	else:
		soup = BeautifulSoup(content, 'lxml')
		bin_urls = soup.find_all('a', {'href':re.compile(r'.*?(gz)|(zip)')})	# tar.gz  tgz  zip gtar.gz
		for i, url in enumerate(bin_urls):
			# bin_urls[i] = r'http://chaosscripting.net' + url.attrs['href']
			bin_urls[i] = r'http://archive.robocup.info' + url.attrs['href']
	return bin_urls

# 为了多线程的使用
def download_bin(param):
	local_path = param.get('local_path')
	bin_url = param.get('bin_url')
	bin_name = os.path.basename(bin_url)
	socket.setdefaulttimeout(30)
	if os.path.exists(local_path + '/' + bin_name):
		print('{} already exists'.format(bin_name))
		return
	try:
		print('downloading {}'.format(bin_name))
		urllib.request.urlretrieve(bin_url, '{}/{}'.format(local_path, bin_name))	# reporthook=report
		print('{} download complete'.format(bin_name))
	except:
		print("downloading " + bin_name + ' timeout')
		os.remove(local_path + '/' + bin_name)


def download_bins(page):
	print('---------------------start downloading ' + str(page) + ' binary---------------------')
	bin_urls = get_bin_urls(page)
	local_path = './2D_Binsries/{}'.format(str(page))
	if not os.path.exists('./2D_Binsries'): os.mkdir('./2D_Binsries')
	if not os.path.exists(local_path): os.mkdir(local_path)
	if bin_urls is None or len(bin_urls) == 0: return
	'''
	for bin_url in bin_urls:
		bin_name = os.path.basename(bin_url)
		print(local_path + '/' + bin_name[0])
		socket.setdefaulttimeout(30)
		if os.path.exists(local_path + '/' + bin_name):
			print('{} already exists'.format(bin_name))
			continue
		try:
			print('downloading {}'.format(bin_name))
			urllib.request.urlretrieve(bin_url, '{}/{}'.format(local_path, bin_name), reporthook = report)
		except:
			print("downloading " + bin_name + ' timeout')
			os.remove(local_path + '/' + bin_name)
	'''

	# 使用多线程
	params = []
	for bin_url in bin_urls:
		params.append({'local_path': local_path, 'bin_url': bin_url})
	Pool().map(download_bin, params)
	print('---------------------' + str(page) + 'binary download complete---------------------')


def get_tdp_urls(page):
	url = 'http://archive.robocup.info/soccer/simulation/2D/tdps/RoboCup/{}/'.format(str(page))
	# url = r'http://chaosscripting.net/files/competitions/RoboCup/WorldCup/' + str(page) + '/2DSim/tdps/'
	headers = {'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = urllib.request.Request(url, headers = headers)
	try:
		html = urllib.request.urlopen(request, timeout = 30).read().decode('utf-8')
	except:
		print('the first crawl failed, try crawl second times')
		try:
			html = urllib.request.urlopen(request, timeout = 20).read().decode('utf-8')
		except:
			print('the second crawl failed')
			return None
	if html is None:
		print('URL is not found!')
		return None
	else:
		soup = BeautifulSoup(html, 'lxml')
		tdp_urls = soup.find_all('a', {'href':re.compile(r'.*?pdf')})
		for i, url in enumerate(tdp_urls):
			# tdp_urls[i] = r'http://chaosscripting.net' + url.attrs['href']
			tdp_urls[i] = 'http://archive.robocup.info' + url.attrs['href']
	return tdp_urls


def download_tdps(page):
	print('---------------------start downloading ' + str(page) + ' TDP---------------------')
	tdp_urls = get_tdp_urls(page)
	local_path = './2D_TDP/' + str(page)
	if not os.path.exists('./2D_TDP'): os.mkdir('./2D_TDP')
	if not os.path.exists(local_path): os.mkdir(local_path)
	if tdp_urls is None or len(tdp_urls) == 0: return
	for tdp_url in tdp_urls:
		tdp_name = os.path.basename(tdp_url)
		socket.setdefaulttimeout(30)
		if os.path.exists(local_path + '/' + tdp_name):
			print('{} already exists'.format(tdp_name))
			continue
		print('downloading ' + tdp_name)
		try:
			urllib.request.urlretrieve(tdp_url, local_path + '/' + tdp_name)
		except:
			print('downloading ' + tdp_name + ' timeout')
	print('---------------------' + str(page) + ' TDP download complete---------------------')


def init_download_bins():
	for page in range(2017, 2016, -1):	# 1996~2016
		download_bins(page)
	print('---------------------all binary download complete---------------------')


def init_download_tdps():
	# for page in range(2016, 2001, -1):		#2002-2016
	# 	if page == 2013:
	# 		continue
	# 	download_tdps(page)

	# 多进程下载
	pages = [x for x in range(2017, 2001, -1) if x != 2013] 	#2002-2017
	Pool().map(download_tdps, pages)
	print('---------------------all TDP download complete---------------------')

def main():
	init_download_bins()
	# init_download_tdps()

if __name__ == '__main__':
    main()

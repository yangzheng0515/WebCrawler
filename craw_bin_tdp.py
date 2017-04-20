# _*_ coding:utf-8 _*_
'''
author: yz
time: 2017/3/2

从http://chaosscripting.net/files/competitions/RoboCup/WorldCup/ 中爬取RoboCup2d近二十年来的TDP和Bin
Python3
需要下载bs4库 sudo apt-get install python3-bs4
可在main中设置下载bin还是tdp
可在download_bins、download_tdps中设置需要下载的年份
可能因网络或其他原因导致下载不完全，可在不改变目录的情况下执行几次
'''
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import re
import os
import sys
import socket


def get_bin_urls(page):
	url = r'http://chaosscripting.net/files/competitions/RoboCup/WorldCup/' + str(page) + '/2DSim/binaries/'
	headers = {'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = urllib.request.Request(url, headers = headers)
	try:
		html = urllib.request.urlopen(request, timeout = 30).read().decode('utf-8')
	except:
		print('first craw failed')
		print('try second craw')
		try:
			html = urllib.request.urlopen(request, timeout = 20).read().decode('utf-8')	
		except:
			print('second craw failed')
			return None
	if html is None:
		print('URL is not found!')
		return None
	else:
		soup = BeautifulSoup(html, 'lxml')
		bin_urls = soup.find_all('a', {'href':re.compile(r'.*?(gz)|(zip)')})	# .tar.gz  .tgz  .zip .gtar.gz
		i = 0
		for url in bin_urls:
			bin_urls[i] = r'http://chaosscripting.net' + url.attrs['href']
			i += 1
	return bin_urls

def download_bin(page):
	bin_urls = get_bin_urls(page)
	local_path = './2D_Binsries/' + str(page)
	if not os.path.exists('./2D_Binsries'):
		os.mkdir('./2D_Binsries')
	if not os.path.exists(local_path):
		os.mkdir(local_path)
	if bin_urls is None or len(bin_urls) == 0:
		pass
	else:
		for bin_url in bin_urls:
			bin_name = os.path.basename(bin_url)
			#print(local_path + '/' + bin_name[0])
			socket.setdefaulttimeout(30)
			if os.path.exists(local_path + '/' + bin_name):
				print('已存在' + bin_name)
			else:
				try:
					print('正在下载'+bin_name)
					urllib.request.urlretrieve(bin_url, local_path + '/' + bin_name)
				except:
					print("下载" + bin_name + '超时')
					os.remove(local_path + '/' + bin_name)
					continue
	
def get_tdp_urls(page):
	url = r'http://chaosscripting.net/files/competitions/RoboCup/WorldCup/' + str(page) + '/2DSim/tdps/'
	headers = {'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	request = urllib.request.Request(url, headers = headers)
	try:
		html = urllib.request.urlopen(request, timeout = 30).read().decode('utf-8')
	except:
		print('first craw failed')
		print('try second craw')
		try:
			html = urllib.request.urlopen(request, timeout = 20).read().decode('utf-8')
		except:
			print('second craw failed')
			return None
	if html is None:
		print('URL is not found!')
		return None
	else:
		soup = BeautifulSoup(html, 'lxml')
		tdp_urls = soup.find_all('a', {'href':re.compile(r'.*?pdf')})	
		i = 0
		for url in tdp_urls:
			tdp_urls[i] = r'http://chaosscripting.net' + url.attrs['href']
			i += 1
	return tdp_urls

def download_tdp(page):
	tdp_urls = get_tdp_urls(page)
	local_path = './2D_TDP/' + str(page)
	if not os.path.exists('./2D_TDP'):
		os.mkdir('./2D_TDP')
	if not os.path.exists(local_path):
		os.mkdir(local_path)
	if tdp_urls is None or len(tdp_urls) == 0:
		pass
	else:
		for tdp_url in tdp_urls:
			tdp_name = os.path.basename(tdp_url)
			socket.setdefaulttimeout(30)
			if os.path.exists(local_path + '/' + tdp_name):
				print('已存在' + tdp_name)
			else:	
				print('正在下载'+tdp_name)			
				try:
					urllib.request.urlretrieve(tdp_url, local_path + '/' + tdp_name)
				except:
					print('下载' + tdp_name + '超时')
					continue

def download_bins():
	for page in range(2016, 1995, -1):	# 1996~2016
		print('---------------------开始下载' + str(page) + '年Bin---------------------')
		download_bin(page)
		print('---------------------' + str(page) + '年Bin下载完成---------------------')
	print('-------------------------------BIN下载完成-------------------------------')

def download_tdps():
	for page in range(2016, 2001, -1):		#2002-2016
		if page == 2013:
			continue
		print('---------------------开始下载' + str(page) + '年TDP---------------------')
		download_tdp(page)
		print('---------------------' + str(page) + '年TDP下载完成---------------------')
	print('-------------------------------TDP下载完成-------------------------------')

def main():
	download_tdps()
	#download_bins()	
	

if __name__ == '__main__':
	main()

import urllib.request
import random

url = 'http://www.whatismyip.com.tw'
# url = 'http://www.ip138.com/'
# url = 'http://www.ip.cn/'

iplist = ['61.172.249.96:80','58.222.254.11:3128','61.185.219.126:3128','218.247.161.37:80']

proxy_support = urllib.request.ProxyHandler({'http':random.choice(iplist)})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = urllib.request.Request(url, headers = headers)
html = urllib.request.urlopen(page).read().decode('utf-8')
#html = opener.open(page).read().decode('utf-8')

print(html)

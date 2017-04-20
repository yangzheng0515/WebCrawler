import urllib
import http.cookiejar

# filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)
# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
# postdata = urllib.parse.urlencode({
# 			'username':'***',
# 			'passward':'***'
# 		}).encode('utf-8')

# loginUrl = 'https://www.douban.com/'
# result = opener.open(loginUrl,postdata)
# cookie.save(ignore_discard=True, ignore_expires=True)
# gradeUrl = 'https://www.douban.com/people/157408789/'
# result = opener.open(gradeUrl)
# print(result.read().decode('utf-8'))


#创建MozillaCookieJar实例对象
cookie = http.cookiejar.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
#创建请求的request
req = urllib.request.Request("https://www.douban.com/")
#利用urllib2的build_opener方法创建一个opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
response = opener.open(req)
print(response.read())
